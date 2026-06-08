##
# @tags: howto, fundamental, properties
# @title: How to read all properties
##
# Iterates over all visible properties on a component and prints
# their names, values, and read-only status.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        simulator = daq_utils.setup_simulator()

        fb = simulator.add_function_block("RefFBModuleStatistics")
        print(f"Properties on: {fb.name}\n")

        for prop in fb.visible_properties:
            value = fb.get_property_value(prop.name)
            ro = " (read-only)" if prop.read_only else ""
            print(f"  {prop.name}: {value}{ro}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)