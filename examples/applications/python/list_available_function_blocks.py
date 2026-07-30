##
# @tags: howto, function-blocks
# @title: How to list the function block types an instance can add
##
# Prints the id, name and description of every function block type the
# instance's loaded modules offer.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        instance = daq.Instance()
        daq_utils.print_types("Available function block types",
                              instance.available_function_block_types)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
