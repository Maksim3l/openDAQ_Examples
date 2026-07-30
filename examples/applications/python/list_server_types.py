##
# @tags: howto, servers
# @title: How to list the server types an instance can host
##
# Prints the id, name and description of every server type the instance's
# loaded modules offer.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        instance = daq.Instance()
        daq_utils.print_types("Available server types",
                              instance.available_server_types)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
