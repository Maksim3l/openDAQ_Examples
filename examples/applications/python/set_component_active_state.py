##
# @tags: howto, component-tree, active
# @title: How to set a component's active state
##
# Deactivates a channel, reads the active state of the channel and of the
# signals under it, then activates it again.
##

import sys
import Utils.daq_utils as daq_utils


def print_state(channel):
    print(f"{channel.name}: active={bool(channel.active)}")
    for signal in channel.signals:
        print(f"  {signal.name}: active={bool(signal.active)}"
              f" parent_active={bool(signal.parent_active)}")


if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        daq_utils.exit_if_empty(device.channels, "Device has no channel")
        channel = device.channels[0]

        print_state(channel)

        # Deactivating a component deactivates what sits under it. The children
        # report through parent_active that it came from above them.
        channel.active = False
        print()
        print_state(channel)

        channel.active = True
        print()
        print_state(channel)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
