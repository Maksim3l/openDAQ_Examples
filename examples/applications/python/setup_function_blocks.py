##
# @tags: howto, function-blocks, signals, input-ports
# @title: How to connect signals to input ports
##
# Connects a device signal to a function block's input port and
# reads the processed output.
##

import time
import opendaq as daq
import sys
import Utils.daq_utils as daq_utils


if __name__ == "__main__":
    try:
        simulator = daq_utils.setup_simulator()

        signals = simulator.get_signals_recursive()
        daq_utils.exit_if_empty(signals, "No signals found")

        signal = signals[0]
        print(f"Using signal: {signal.name}")

        scaling_fb = simulator.add_function_block("RefFBModuleScaling")

        scaling_fb.input_ports[0].connect(signal)
        print(f"Connected {signal.name} -> {scaling_fb.input_ports[0].name}")

        scaling_fb.set_property_value("scale", 10)
        print(f"Set scale to 10")

        # Read a few samples from the scaled output
        reader = daq.StreamReader(scaling_fb.signals[0])
        time.sleep(0.2)
        values = reader.read(10)
        print(f"\nScaled output ({len(values)} samples):")
        for v in values[:5]:
            print(f"  {v}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)