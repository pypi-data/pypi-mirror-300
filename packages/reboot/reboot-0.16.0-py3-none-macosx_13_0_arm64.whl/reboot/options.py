from google.protobuf.descriptor import Descriptor
from google.protobuf.descriptor_pb2 import (
    MessageOptions,
    MethodOptions,
    ServiceOptions,
)
from rbt.v1alpha1 import options_pb2
from typing import Optional


def get_state_options(
    options: MessageOptions,
) -> Optional[options_pb2.StateOptions]:
    """Takes a proto descriptor of options specified on a message, and extracts
    the reboot.StateOptions, if such an option is set.
    """
    # This is the proto API for accessing our custom options used in the
    # given `MessageOptions`.
    #
    # We don't want a default `reboot.StateOptions` as we need to
    # know where or not the option was explicitly set so we return
    # `None` in the event it was not set.
    if options_pb2.state in options.Extensions:
        return options.Extensions[options_pb2.state]
    else:
        return None


def is_reboot_state(message: Descriptor) -> bool:
    """Check if the message is a Reboot state.

    A reboot state MUST have the StateOptions annotation.
    """

    return get_state_options(message.GetOptions()) is not None


def get_method_options(options: MethodOptions) -> options_pb2.MethodOptions:
    """Takes a proto descriptor of options specified on a method, and extracts
    the reboot.MethodOptions, if such an option is set.
    """
    # This is the proto API for accessing our custom options used in the
    # given `MethodOptions`. Returns an empty reboot.MethodOptions if no
    # option is set, which means its options will default to the proto
    # defaults for their field types.
    return options.Extensions[options_pb2.method]


def get_service_options(options: ServiceOptions) -> options_pb2.ServiceOptions:
    """Takes a proto descriptor of options specified on a service, and extracts
    the reboot.ServiceOptions, if such an option is set.
    """
    # This is the proto API for accessing our custom options used in the
    # given `ServiceOptions`. Returns an empty reboot.ServiceOptions if no
    # option is set, which means its options will default to the proto
    # defaults for their field types.
    return options.Extensions[options_pb2.service]
