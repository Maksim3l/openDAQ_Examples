##
# @tags: howto, fundamental, discovery, device
# @title: How to discover devices and connect
##
# Discovers all available devices, groups them by whether they
# advertise server capabilities, and connects to each one.
##

import sys
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        instance = daq.Instance()

        available_devices = instance.available_devices
        if not available_devices:
            print("No devices found", file=sys.stderr)
            print("exit 1")
            sys.exit(1)

        # Devices that advertise server capabilities support openDAQ
        # protocol connections. Those without are provided directly
        # by modules loaded in this instance.
        with_servers = []
        without_servers = []
        for device_info in available_devices:
            if len(device_info.server_capabilities):
                with_servers.append(device_info)
            else:
                without_servers.append(device_info)

        print("Devices with server capabilities:")
        for info in with_servers:
            print(f"\n  {info.name}:")
            daq_utils.print_property_object(info, 2)

        print("\nDevices without server capabilities:")
        for info in without_servers:
            print(f"\n  {info.name}:")
            daq_utils.print_property_object(info, 2)

        # add_device takes the connection string from the DeviceInfo.
        print("\nConnecting to devices...")
        connected = []
        for info in available_devices:
            device = instance.add_device(info.connection_string)
            connected.append(device)
            print(f"  Connected: {device.name}")

        print(f"\n{len(connected)} device(s) connected")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)