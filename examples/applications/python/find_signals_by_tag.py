##
# @tags: howto, signals, tags
# @title: How to find signals by tag
##
# Searches a device's signals for a required tag and prints what the search
# returned.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

TAG = "AnalogInput"

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        # The search walks the whole tree under the device and keeps only the
        # signals carrying every tag in the filter.
        signals = device.get_signals_recursive(
            daq.RequiredTagsSearchFilter([TAG]))
        daq_utils.exit_if_empty(signals, f"No signal tagged '{TAG}'")

        print(f"Signals tagged '{TAG}': {len(signals)}")
        for signal in signals:
            print(f"  {signal.name}")
            print(f"    global id: {signal.global_id}")
            print(f"    tags:      {list(signal.tags.list)}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
