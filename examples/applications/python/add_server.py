##
# @tags: howto, servers
# @title: How to add and remove a server
##
# Adds an openDAQ native streaming server to an instance, lists the running
# servers, and removes it again.
##

import sys
import opendaq as daq

if __name__ == "__main__":
    try:
        instance = daq.Instance()
        print(f"Running servers: {len(instance.servers)}")

        server = instance.add_server("OpenDAQNativeStreaming", None)
        print(f"\nAdded: {server.id}")
        for running in instance.servers:
            print(f"  {running.id}")

        # A server publishes the instance's own tree, so a client that connects
        # to it sees whatever devices the instance holds.
        instance.remove_server(server)
        print(f"\nRunning servers: {len(instance.servers)}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
