#!/usr/bin/env python3
import os
from dataclasses import asdict, dataclass
from google.api import annotations_pb2
from google.protobuf.descriptor import (
    Descriptor,
    FieldDescriptor,
    FileDescriptor,
    MethodDescriptor,
    ServiceDescriptor,
)
from google.protobuf.descriptor_pb2 import (
    FileDescriptorProto,
    ServiceDescriptorProto,
)
# TODO: Dependency not recognized in git-submodule for some reason.
from pyprotoc_plugin.helpers import (  # type: ignore[import]
    add_template_path,
    load_template,
)
from pyprotoc_plugin.plugins import ProtocPlugin  # type: ignore[import]
from rbt.v1alpha1 import options_pb2
from reboot.aio.types import service_to_state_type
from reboot.cli import terminal
from reboot.options import (
    get_method_options,
    get_service_options,
    is_reboot_state,
)
from typing import Literal, Optional, Sequence

# NOTE: we need to add the template path so we can test
# `RebootProtocPlugin` even when we're not '__main__'.
add_template_path(os.path.join(__file__, '../templates/'))

Feature = Literal[
    'reader',
    'writer',
    'transaction',
    'error',
    'streaming',
    'workflow',
]


class UserProtoError(Exception):
    """Exception raised in case of a malformed user-provided proto file."""
    pass


@dataclass(kw_only=True)
class PluginSpecificData:
    template_filename: str
    output_filename_suffix: str
    supported_features: list[Feature]
    only_generates_with_reboot_services: bool = True
    exclude_google_and_reboot_system_generation: bool = True


ProtoType = str


@dataclass
class ProtoMethodOptions:
    kind: str
    constructor: bool
    state_streaming: bool
    has_errors: bool


@dataclass
class BaseMethodOptions:
    proto: ProtoMethodOptions


@dataclass
class ProtoMethod:
    name: str
    client_streaming: bool
    server_streaming: bool


@dataclass
class BaseMethod:
    proto: ProtoMethod
    options: BaseMethodOptions


@dataclass
class ProtoServiceOptions:
    state_name: str


@dataclass
class BaseServiceOptions:
    proto: ProtoServiceOptions


@dataclass
class ProtoService:
    name: str
    has_constructor: bool
    requires_constructor: bool


@dataclass
class BaseService:
    proto: ProtoService
    # The following is a Sequence, not list, to make it covariant:
    #   https://mypy.readthedocs.io/en/stable/common_issues.html#variance
    methods: Sequence[BaseMethod]
    options: BaseServiceOptions


@dataclass
class ProtoFile:
    package_name: str
    file_name: str
    # List of all messages and enums in the proto file.
    messages_and_enums: list[str]
    # List of all messages that are Reboot state data types.
    states: list[str]


@dataclass
class BaseFile:
    proto: ProtoFile
    # The following is a Sequence, not list, to make it covariant:
    #   https://mypy.readthedocs.io/en/stable/common_issues.html#variance
    services: Sequence[BaseService]


class RebootProtocPlugin(ProtocPlugin):

    @staticmethod
    def _get_state_name_from_service_name(service_name: str) -> Optional[str]:
        if not service_name.endswith('Interface'):
            return None
        state_name = service_name[:-len('Interface')]
        state_name = state_name[state_name.rfind('.') + 1:]

        return state_name

    @staticmethod
    def _proto_reboot_services(
        file: FileDescriptor, state_names: list[str]
    ) -> list[ServiceDescriptorProto]:
        reboot_services = []
        reboot_service_found_by_state_name: dict[str, bool] = {
            state_name: False for state_name in state_names
        }

        def _check_reboot_requirements(
            service: ServiceDescriptor,
            is_reboot_service: bool,
            state_name: Optional[str],
            has_state_in_current_file: bool,
        ) -> None:
            for method in service.methods:
                is_reboot_method = False
                for _, value in method.GetOptions().ListFields():
                    if isinstance(value, options_pb2.MethodOptions):
                        is_reboot_method = True

                if is_reboot_service and not is_reboot_method:
                    raise ValueError(
                        "Missing Reboot method annotation for "
                        f"'{service.full_name}/{method.name}'"
                    )
                elif not is_reboot_service and is_reboot_method:
                    if state_name is not None:
                        # Assuming both names are in the same package and the
                        # state message exists, but annotations are missing.
                        if has_state_in_current_file:
                            raise ValueError(
                                f"Reboot interface '{service.full_name}' has "
                                f"matching 'message {state_name}', but that "
                                "message is missing the Reboot state "
                                "annotation"
                            )
                        # Error uses 'service_to_state_type' to get the same
                        # package name, when 'state_name' contains the state
                        # message name.
                        raise ValueError(
                            "Found Reboot method annotations in "
                            f"'{service.full_name}/{method.name}', "
                            f"'{service.full_name}' is a Reboot interface "
                            "for the "
                            f"'{service_to_state_type(service.full_name)}' "
                            f"state, but there is no 'message {state_name}' in "
                            "this proto file."
                        )
                    else:
                        # At this point we can't guess the state name, so we produce
                        # a general error message.
                        raise ValueError(
                            "Found Reboot method annotations in "
                            f"'{service.full_name}/{method.name}', but "
                            f"'{service.full_name}' is not a Reboot service. "
                            "Reboot services are interfaces and must be "
                            "named '[...]Interface"
                        )

                if is_reboot_method and method.name[0].islower():
                    # Reboot method names must start with an uppercase letter,
                    # to avoid name clashes with Python modules in the Reboot
                    # generated code (e.g. `rpc reboot` would shadow the
                    # `reboot` module).
                    raise ValueError(
                        f"Reboot method '{service.full_name}/{method.name}' "
                        "has illegal name: all Reboot RPC method names must "
                        "start with an uppercase letter."
                    )

        def _convert_service_to_proto(
            file: FileDescriptor, service: ServiceDescriptor
        ) -> ServiceDescriptorProto:
            service_descriptor_proto = ServiceDescriptorProto()
            service.CopyToProto(service_descriptor_proto)
            return service_descriptor_proto

        for service in file.services_by_name.values():
            state_name = RebootProtocPlugin._get_state_name_from_service_name(
                service.full_name
            )

            has_state_in_file_states = state_name in state_names

            is_reboot_service = state_name is not None and has_state_in_file_states

            _check_reboot_requirements(
                service,
                is_reboot_service,
                state_name,
                RebootProtocPlugin._is_message_in_file(state_name, file),
            )

            if is_reboot_service:
                assert state_name is not None
                reboot_service_found_by_state_name[state_name] = True
                reboot_services.append(
                    _convert_service_to_proto(file, service)
                )

        for state_name, found in reboot_service_found_by_state_name.items():
            if not found:
                raise ValueError(
                    f"Missing Reboot service for state '{state_name}'. "
                    "Define a service with the name "
                    f"'{state_name}Interface' in the same proto file "
                    "where your state is defined."
                )
        return reboot_services

    @staticmethod
    def plugin_specific_data() -> PluginSpecificData:
        """Returns the plugin-specific data for the plugin."""
        raise NotImplementedError

    @classmethod
    def _proto_state_names(
        self,
        file: FileDescriptor,
    ) -> list[str]:
        """Helper to extract name of all messages that are Reboot state data
        types from file descriptor.
        """
        return [
            name for name, descriptor in file.message_types_by_name.items()
            if is_reboot_state(descriptor)
        ]

    @classmethod
    def _is_message_in_file(
        self,
        message_name: Optional[str],
        file: FileDescriptor,
    ) -> bool:
        if message_name is None:
            return False
        return message_name in file.message_types_by_name

    @classmethod
    def _proto_message_and_enum_names(
        self,
        file: FileDescriptor,
    ) -> list[str]:
        """Helper to extract name of all messages and enums from file descriptor.
        """
        # NOTE: `message_types_by_name` is undefined if no messages are present.
        try:
            # Include *only* top-level messages and enums in the file. Accessing
            # nested structures is supported through parent message, which will
            # be included in the list of.
            import_messages_and_enums = list(
                file.message_types_by_name.keys()
            ) + list(file.enum_types_by_name.keys())

            return import_messages_and_enums
        except AttributeError as e:
            assert 'message_types_by_name' in str(e)
            return []

    def template_data(
        self,
        proto_file: FileDescriptorProto,
    ) -> BaseFile:
        file = self.pool.FindFileByName(proto_file.name)
        if file.package == '':
            raise UserProtoError(
                f"{file.name} is missing a (currently) required 'package'"
            )

        directory = os.path.dirname(file.name)
        package_directory = file.package.replace('.', os.path.sep)
        if package_directory != directory:
            raise UserProtoError(
                f"Proto file '{file.name}' has package '{file.package}', but "
                "based on the file's path the expected package was "
                f"'{directory.replace(os.path.sep, '.')}'. 'rbt protoc' "
                "expects the package to match the directory structure. Check "
                "that the API base directory is correct, and if so, adjust "
                "either the proto file's location or its package."
            )

        reboot_services = self._proto_reboot_services(
            file,
            self._proto_state_names(file),
        )

        # Validate that only legacy gRPC services are using the
        # `google.api.http` annotations.
        for service in proto_file.service:
            if service not in reboot_services:
                # Legacy gRPC services are allowed to have `google.api.http`
                # annotations.
                continue
            for method in service.method:
                if method.options.HasExtension(annotations_pb2.http):
                    # The user has specified HTTP annotations on a Reboot
                    # service's methods. We don't support this (yet).
                    #
                    # TODO(rjh): consider what it would take to allow Reboot
                    #            services to have their own `google.api.http`
                    #            annotations; at least singletons.
                    raise UserProtoError(
                        f"Service '{service.name}' method '{method.name}' "
                        "has a 'google.api.http' annotation. This is only "
                        "supported for legacy gRPC services, not for Reboot "
                        "methods. Let the maintainers know about your use case "
                        "if you feel this is a limitation!"
                    )

        template_data = self.plugin_template_data(proto_file)
        # 'template_data.services' only contains Reboot services. If the
        # `proto_file` does not contain reboot services, i.e. dependencies,
        # return template_data early so it can be passed to non-Reboot
        # templates that might need it.
        if len(template_data.services) == 0:
            return template_data

        self.validate_features(template_data)

        for service in template_data.services:
            for method in service.methods:
                if method.proto.client_streaming and method.options.proto.kind != 'reader':
                    raise UserProtoError(
                        'Client streaming only supported for readers'
                    )
                if method.proto.server_streaming and method.options.proto.kind != 'reader':
                    raise UserProtoError(
                        'Server streaming only supported for readers'
                    )

        return template_data

    def _analyze_proto_file(self, proto_file: FileDescriptor) -> ProtoFile:
        return ProtoFile(
            package_name=proto_file.package,
            file_name=proto_file.name,
            messages_and_enums=self._proto_message_and_enum_names(proto_file),
            states=self._proto_state_names(proto_file),
        )

    def _analyze_proto_service_options(
        self, service: ServiceDescriptor
    ) -> ProtoServiceOptions:
        state_name = RebootProtocPlugin._get_state_name_from_service_name(
            service.full_name
        )

        assert state_name is not None

        return ProtoServiceOptions(state_name=state_name)

    def _is_default_constructible(self, service: ServiceDescriptor) -> bool:
        service_options = get_service_options(service.GetOptions())
        return service_options.default_constructible

    def _is_method_constructor(self, method: MethodDescriptor) -> bool:
        method_options = get_method_options(method.GetOptions())
        kind: Optional[str] = method_options.WhichOneof('kind')
        if kind is None:
            raise UserProtoError(
                f"'{method.name}' is missing the required Reboot annotation 'kind'"
            )

        return kind in [
            'writer', 'transaction'
        ] and getattr(method_options, kind).HasField('constructor')

    @classmethod
    def _is_map_field(
        cls, message: Descriptor, field: FieldDescriptor
    ) -> bool:
        # Protobuf encodes its `map` type as a repeated message type name
        # `{${Field}Entry}`, which is an inner type of the message with the
        # same name as the field.
        field_camelcase_name = ''.join(
            component.capitalize() for component in field.name.split('_')
        )
        return (
            field.type == FieldDescriptor.TYPE_MESSAGE and
            field.label == FieldDescriptor.LABEL_REPEATED and
            field.message_type.containing_type == message and
            field.message_type.name == f'{field_camelcase_name}Entry'
        )

    def _analyze_proto_service(
        self,
        service_proto: ServiceDescriptorProto,
        service_descriptor: ServiceDescriptor,
    ) -> ProtoService:
        has_constructor = False
        requires_constructor = False

        if not self._is_default_constructible(service_descriptor):
            for method in service_descriptor.methods:
                if self._is_method_constructor(method):
                    has_constructor = True
                    requires_constructor = True
                    break

        return ProtoService(
            name=service_proto.name,
            has_constructor=has_constructor,
            requires_constructor=requires_constructor,
        )

    def _analyze_proto_method(self, method: MethodDescriptor) -> ProtoMethod:
        return ProtoMethod(
            name=method.name,
            client_streaming=method.client_streaming,
            server_streaming=method.server_streaming,
        )

    def _analyze_proto_method_options(
        self,
        method: MethodDescriptor,
        streaming: bool,
    ) -> ProtoMethodOptions:
        method_options = get_method_options(method.GetOptions())
        kind: Optional[str] = method_options.WhichOneof('kind')

        if kind is None:
            raise UserProtoError(
                f"'{method.name}' is missing the required Reboot annotation 'kind'"
            )

        state_streaming = streaming

        if kind == 'reader':
            if (
                method_options.reader.state ==
                options_pb2.ReaderMethodOptions.State.STREAMING
            ):
                state_streaming = True
            elif (
                method_options.reader.state ==
                options_pb2.ReaderMethodOptions.State.UNARY
            ):
                state_streaming = False

        return ProtoMethodOptions(
            kind=kind,
            constructor=self._is_method_constructor(method),
            state_streaming=state_streaming,
            has_errors=len(method_options.errors) > 0,
        )

    def process_file(self, proto_file: FileDescriptorProto) -> None:
        try:
            if (
                proto_file.syntax != "proto3"
                # Special case: the `descriptor.proto` doesn't report a syntax,
                #               but we know we can handle it.
                and proto_file.name != "google/protobuf/descriptor.proto"
            ):
                raise UserProtoError(
                    f"Unsupported: not a proto3 file. "
                    "Reboot only supports proto files that set "
                    "'syntax=\"proto3\";', but got "
                    f"'syntax=\"{proto_file.syntax}\";'"
                )

            template_data = self.template_data(proto_file)

            # Check if file has any Reboot services and only generate if the
            # plugin wants to and the service is user-defined.
            if len(template_data.services) == 0:
                if self.plugin_specific_data(
                ).only_generates_with_reboot_services:
                    return None

                if self._is_google_or_reboot_package(
                    proto_file.package
                ) and self.plugin_specific_data(
                ).exclude_google_and_reboot_system_generation:
                    return None

                # No Reboot services but plugin still wants to generate code.
                output_file = self.response.file.add()
                output_file.name = template_data.proto.file_name.replace(
                    '.proto',
                    self.plugin_specific_data().output_filename_suffix,
                )
                output_file.content = self.template_render(template_data)
                return output_file

            for service in template_data.services:
                if len(service.methods) == 0:
                    raise UserProtoError(
                        f"Service '{service.proto.name}' has no rpc methods specified. "
                        "Complete your proto file."
                    )

            content = self.template_render(template_data)
            output_file = self.response.file.add()
            output_file.name = template_data.proto.file_name.replace(
                '.proto',
                self.plugin_specific_data().output_filename_suffix,
            )
            output_file.content = content

        except (UserProtoError, ValueError) as error:
            # NOTE: we catch `ValueError` here because we're using methods from
            # `options.py` that might raise `ValueError` in response to
            # malformed input.
            # We re-raise any error as a `UserProtoError`
            # but with additional information in the error message.
            raise UserProtoError(
                f"Error processing '{proto_file.name}': {error}"
            ) from error

    def plugin_template_data(
        self, proto_file: FileDescriptorProto
    ) -> BaseFile:
        raise NotImplementedError

    def validate_features(self, template_data: BaseFile) -> None:
        """Raises an error if not all user-requested features are implemented.
        """
        feature_set_in_template_data = set()

        for service in template_data.services:
            for method in service.methods:
                feature_set_in_template_data.add(method.options.proto.kind)
                if method.options.proto.has_errors is True:
                    feature_set_in_template_data.add('error')
                if method.options.proto.state_streaming or method.proto.client_streaming or method.proto.server_streaming:
                    feature_set_in_template_data.add('streaming')

        supported_feature_set = set(
            self.plugin_specific_data().supported_features
        )

        if not feature_set_in_template_data.issubset(supported_feature_set):
            terminal.fail(
                'You are attempting to use Reboot features in your .proto '
                'file that are not yet supported.\n'
                '\n'
                f'Unsupported features: {feature_set_in_template_data - supported_feature_set}'
            )

    def get_file_for_message_name(
        self,
        message_name: str,
        current_file: FileDescriptor,
    ) -> FileDescriptor:
        if '.' not in message_name:
            # If we don't have a package name, assume it is the same
            # package as the current file.
            package_name = current_file.package
            message_name = f'{package_name}.{message_name}'

        try:
            return self.pool.FindFileContainingSymbol(message_name)
        except KeyError as e:
            raise UserProtoError(
                f"Cannot resolve message type: '{message_name}'"
            ) from e

    def template_render(
        self,
        template_data: BaseFile,
    ) -> str:
        template = load_template(
            self.plugin_specific_data().template_filename,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            extensions=['jinja2_strcase.StrcaseExtension'],
        )

        return template.render(asdict(template_data))
