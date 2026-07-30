##
# @tags: howto, instance
# @title: How to create an instance
##
# Creates an instance and prints the device types its loaded modules can add.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        instance = daq.Instance()
        print(f"Instance: {instance.name}\n")

        # Device types come from the modules the instance loaded. They are what
        # can be added, not what is reachable right now. A connection string
        # starting with a type's prefix is handed to that type's module.
        daq_utils.print_types("Available device types",
                              instance.available_device_types)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
