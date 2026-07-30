##
# @tags: howto, device, status
# @title: How to read a device's info and status
##
# Connects to a device over the openDAQ native configuration protocol and prints
# its identification fields, its custom info fields and its statuses.
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

        info = device.info
        print(f"{info.name}")
        daq_utils.print_field("manufacturer", info.manufacturer)
        daq_utils.print_field("model", info.model)
        daq_utils.print_field("serial number", info.serial_number)
        daq_utils.print_field("device class", info.device_class)
        daq_utils.print_field("device revision", info.device_revision)
        daq_utils.print_field("hardware revision", info.hardware_revision)
        daq_utils.print_field("connection string", info.connection_string)

        # Beyond the fields every device info carries, a device can publish
        # fields of its own, listed by name here.
        print("\nCustom info fields:")
        for name in info.custom_info_property_names:
            daq_utils.print_field(name, info.get_property_value(name), width=30)

        print("\nStatuses:")
        for name in device.status_container.statuses.keys():
            daq_utils.print_field(
                name, device.status_container.get_status(name), width=30)

        # Connection statuses are tracked apart from the device's own statuses,
        # one entry per configuration or streaming connection in use.
        print("\nConnection statuses:")
        container = device.connection_status_container
        for name in container.statuses.keys():
            daq_utils.print_field(
                name, container.get_status(name), width=44)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
