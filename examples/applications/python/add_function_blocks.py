##
# @tags: howto, fundamental, function-blocks
# @title: How to add a function block
##
# Lists available function block types, adds one, and prints
# its properties and child components.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        instance = daq.Instance()

        types = instance.available_function_block_types
        daq_utils.exit_if_empty(types, "No function block types available")

        print("Available function block types:")
        for id_, type_ in types.items():
            print("\n" + id_)
            daq_utils.print_struct(type_, 1)

        # Function blocks can be signal processing (e.g. statistics, FFT) or protocol-based.
        type_id = "RefFBModuleStatistics"
        daq_utils.exit_if(type_id not in types, f"{type_id} not available")

        print(f"\nAdding function block: {type_id}")
        fb = instance.add_function_block(type_id)

        print("\nFunction block properties and child components:")
        daq_utils.print_component(fb)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)