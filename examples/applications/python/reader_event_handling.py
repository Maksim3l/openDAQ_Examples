##
# @tags: howto, data-path, events
# @title: How to handle reader events
##
# Reads a signal with a packet reader and separates the event packets from the
# data packets, printing what each event carries.
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

        signal = signals[0]

        # A packet reader hands over the signal's packets as they are, so the
        # events arrive in the same stream as the data instead of being folded
        # into a sample count.
        reader = daq.PacketReader(signal)
        time.sleep(0.5)

        packets = reader.read_all()
        daq_utils.exit_if_empty(packets, f"{signal.name} produced no packets")

        data_packets = 0
        for packet in packets:
            if packet.type == daq.PacketType.Event:
                event = daq.IEventPacket.cast_from(packet)
                print(f"Event: {event.event_id}")
                for key in event.parameters.keys():
                    print(f"  {key}")
            elif packet.type == daq.PacketType.Data:
                data_packets += 1

        print(f"\nData packets: {data_packets}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
