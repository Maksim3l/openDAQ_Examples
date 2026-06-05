##
# @tags: howto, function-blocks, recorder
# @title: How to record data to Parquet
##
# Adds a ParquetRecorder function block, connects a signal,
# records for a few seconds, and lists the output files.
##

import os
import time
import opendaq as daq
import sys
sys.path.append("..")
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        simulator = daq_utils.setup_simulator()

        signals = simulator.get_signals_recursive()
        if not signals:
            print("No signals found", file=sys.stderr)
            print("exit 1")
            sys.exit(1)

        recorder_fb = simulator.add_function_block("ParquetRecorder")
        recorder = daq.IRecorder.cast_from(recorder_fb)

        recorder_fb.input_ports[0].connect(signals[0])
        print(f"Connected {signals[0].name} to recorder")

        recorder_fb.set_property_value("Path", ".")
        
        recorder.start_recording()
        print("Recording for 3 seconds...")
        time.sleep(3)
        recorder.stop_recording()
        print("Stopped recording")

        path = recorder_fb.get_property_value("Path")
        parquet_files = [f for f in os.listdir(path) if f.endswith(".parquet")]
        if parquet_files:
            print(f"\nRecorded files:")
            for f in parquet_files:
                print(f"  {f}")
        else:
            print("No parquet files found", file=sys.stderr)
            print("exit 1")
            sys.exit(1)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)