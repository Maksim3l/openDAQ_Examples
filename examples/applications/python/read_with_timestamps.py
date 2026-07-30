##
# @tags: howto, data-path, timestamps
# @title: How to read signal data with timestamps
##
# Reads samples together with the wall-clock time of each one, instead of the
# raw domain ticks a plain stream reader returns.
##

import sys
import time
import opendaq as daq
import Utils.daq_utils as daq_utils

SAMPLE_COUNT = 5

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        signals = daq_utils.find_signals_by_tag(device, "AnalogInput")
        daq_utils.exit_if_empty(signals, "No signal tagged 'AnalogInput'")

        signal = signals[0]

        # The time reader wraps a stream reader and turns that reader's domain
        # ticks into timestamps using the signal's origin and tick resolution.
        reader = daq.TimeStreamReader(daq.StreamReader(signal))

        deadline = time.time() + 5
        values = []
        timestamps = []
        while len(values) < SAMPLE_COUNT and time.time() < deadline:
            time.sleep(0.2)
            values, timestamps = reader.read_with_timestamps(SAMPLE_COUNT)

        daq_utils.exit_if(len(values) < SAMPLE_COUNT,
                          f"Read {len(values)} of {SAMPLE_COUNT} samples")

        print(f"{signal.name}:")
        for i in range(0, SAMPLE_COUNT):
            print(f"  {timestamps[i]}  {values[i]}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
