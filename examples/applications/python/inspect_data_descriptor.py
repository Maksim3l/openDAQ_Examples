##
# @tags: howto, signals, descriptors
# @title: How to inspect a signal's data descriptor
##
# Prints the descriptor of a signal and of its domain signal: sample type, unit
# and data rule.
##

import sys
import Utils.daq_utils as daq_utils


def print_descriptor(signal):
    descriptor = signal.descriptor
    print(f"{signal.name}:")
    print(f"  sample type: {descriptor.sample_type}")
    if descriptor.unit is not None:
        print(f"  unit:        {descriptor.unit.symbol} ({descriptor.unit.name})")

    rule = descriptor.rule
    print(f"  rule:        {rule.type}")
    # A linear rule carries the delta and start that turn a sample's position
    # into its value; an explicit rule carries every value in the packet.
    if rule.parameters is not None:
        for key, value in rule.parameters.items():
            print(f"    {key}: {value}")


if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        signals = daq_utils.find_signals_by_tag(device, "AnalogInput")
        daq_utils.exit_if_empty(signals, "No signal tagged 'AnalogInput'")

        signal = signals[0]
        print_descriptor(signal)

        if signal.domain_signal is not None:
            print()
            print_descriptor(signal.domain_signal)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
