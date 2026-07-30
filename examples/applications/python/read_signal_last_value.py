##
# @tags: howto, data-path, last-value
# @title: How to read a signal's last value
##
# Reads the most recent value of a signal a few times without opening a reader.
##

import sys
import time
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        signals = daq_utils.find_signals_by_tag(device, "AnalogInput")
        daq_utils.exit_if_empty(signals, "No signal tagged 'AnalogInput'")

        signal = signals[0]

        # The last value is whatever the signal produced most recently, so it
        # stays empty until the device has sent its first packet.
        deadline = time.time() + 5
        while signal.last_value is None and time.time() < deadline:
            time.sleep(0.1)

        daq_utils.exit_if(signal.last_value is None,
                          f"{signal.name} produced no value")

        print(f"{signal.name}:")
        for _ in range(5):
            print(f"  {signal.last_value}")
            time.sleep(0.2)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
