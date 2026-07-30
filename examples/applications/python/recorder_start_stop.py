##
# @tags: howto, function-blocks, recorder
# @title: How to start and stop a recorder
##
# Connects a signal to a recorder function block and reads the recording state
# across a start and a stop.
##

import sys
import time
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        signals = daq_utils.find_signals_by_tag(device, "AnalogInput")
        daq_utils.exit_if_empty(signals, "No signal tagged 'AnalogInput'")

        recorder_fb = device.add_function_block("BasicCsvRecorder")
        recorder_fb.input_ports[0].connect(signals[0])
        recorder_fb.set_property_value("Path", ".")

        # Recording is controlled through IRecorder, which a recorder function
        # block implements alongside the function block interface.
        recorder = daq.IRecorder.cast_from(recorder_fb)
        print(f"Recording: {bool(recorder.is_recording)}")

        recorder.start_recording()
        print(f"Recording: {bool(recorder.is_recording)}")
        time.sleep(1)

        recorder.stop_recording()
        print(f"Recording: {bool(recorder.is_recording)}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
