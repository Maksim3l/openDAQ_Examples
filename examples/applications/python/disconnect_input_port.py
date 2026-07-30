##
# @tags: howto, input-ports, signals
# @title: How to disconnect an input port
##
# Disconnects a connected input port and reads the port's state before and
# after.
##

import sys
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        signals = daq_utils.find_signals_by_tag(device, "AnalogInput")
        daq_utils.exit_if_empty(signals, "No signal tagged 'AnalogInput'")

        fb = device.add_function_block("RefFBModuleScaling")
        port = fb.input_ports[0]

        port.connect(signals[0])
        print(f"{port.name}")
        print(f"  signal:     {port.signal.name}")
        print(f"  connection: {port.connection}")

        port.disconnect()
        print(f"\n{port.name}")
        print(f"  signal:     {port.signal}")
        print(f"  connection: {port.connection}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
