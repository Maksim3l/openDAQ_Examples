##
# @tags: howto, fundamental, properties
# @title: How to change a property value
##
# Reads a property value, changes it, and confirms the update.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        simulator = daq_utils.setup_simulator()

        fb = simulator.add_function_block("RefFBModuleStatistics")
        print(f"Component: {fb.name}")

        prop_name = "BlockSize"
        print(f"{prop_name} before: {fb.get_property_value(prop_name)}")

        fb.set_property_value(prop_name, 20)

        print(f"{prop_name} after:  {fb.get_property_value(prop_name)}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
