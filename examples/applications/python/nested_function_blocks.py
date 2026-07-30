##
# @tags: howto, function-blocks
# @title: How to add nested function blocks
##
# Adds a function block inside another function block, prints it,
# and removes it.
##

import opendaq as daq
import sys
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        instance = daq.Instance()

        statistics_fb = instance.add_function_block("RefFBModuleStatistics")

        nested_types = statistics_fb.available_function_block_types
        daq_utils.exit_if_empty(nested_types, "No nested FB types available")

        # Function blocks can host other function blocks. Adding to
        # an FB works the same as adding to the instance.
        nested_fbs = []
        for fb_type in nested_types.values():
            fb = statistics_fb.add_function_block(fb_type.Id)
            nested_fbs.append(fb)
            print(f"Added nested FB: {fb.name}")

        for fb in nested_fbs:
            statistics_fb.remove_function_block(fb)
            print(f"Removed: {fb.name}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)