##
# @tags: howto, device, operation-mode
# @title: How to set a device's operation mode
##
# Prints the operation modes a device accepts, switches it to each of them, and
# reads the mode back.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        modes = []
        for mode in device.available_operation_modes:
            modes.append(daq.OperationModeType(int(mode)))

        print(f"Device: {device.name}")
        print(f"Current mode: {device.operation_mode}")
        print("Available modes:")
        for mode in modes:
            print(f"  {mode}")

        print()
        for mode in modes:
            device.operation_mode = mode
            print(f"Set to {mode}, reads back {device.operation_mode}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
