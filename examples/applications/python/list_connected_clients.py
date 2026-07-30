##
# @tags: howto, servers, clients
# @title: How to list the clients connected to a device
##
# Connects to a device over the openDAQ native configuration protocol and prints
# the clients the device reports as connected.
##

import sys
import time
import opendaq as daq
import Utils.daq_utils as daq_utils

CONNECTION_STRING = "daq.nd://127.0.0.1"

if __name__ == "__main__":
    try:
        daq_utils.setup_simulator()

        client = daq.Instance()
        device = client.add_device(CONNECTION_STRING)
        time.sleep(1)

        # The list is kept by the device and read through its device info, so it
        # covers every client connected to it, not only this one.
        clients = device.info.connected_clients_info
        print(f"Clients connected to {device.name}: {len(clients)}")

        for entry in clients:
            info = daq.IConnectedClientInfo.cast_from(entry)
            print(f"  {info.protocol_name}")
            print(f"    address:     {info.address}")
            print(f"    host name:   {info.host_name}")
            print(f"    client type: {info.client_type_name}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
