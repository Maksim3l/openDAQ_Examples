##
# @tags: howto, input-ports, signals
# @title: How to connect a signal to an input port
##
# Inspects a function block's input ports, checks whether a port accepts a
# signal, connects it, and reads the connection back off the port.
##

import sys
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        signals = daq_utils.find_signals_by_tag(device, "AnalogInput")
        daq_utils.exit_if_empty(signals, "No signal tagged 'AnalogInput'")

        signal = signals[0]
        fb = device.add_function_block("RefFBModuleScaling")

        print(f"Input ports on {fb.name}:")
        for port in fb.input_ports:
            print(f"  {port.name}")
            # A port that requires a signal will not process anything until one
            # is connected.
            print(f"    requires a signal: {bool(port.requires_signal)}")
            print(f"    connected signal:  {port.signal}")

        port = fb.input_ports[0]
        daq_utils.exit_if(not port.accepts_signal(signal),
                          f"{port.name} does not accept {signal.name}")

        port.connect(signal)
        print(f"\nConnected {signal.name} to {port.name}")
        print(f"  connected signal: {port.signal.name}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
