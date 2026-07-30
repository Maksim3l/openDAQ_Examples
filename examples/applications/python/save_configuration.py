##
# @tags: howto, save-load
# @title: How to save a configuration
##
# Writes a property value, saves the instance configuration to a string, and
# stores it in a file.
##

import sys
import Utils.daq_utils as daq_utils

CONFIG_FILE = "instance_config.json"

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()
        device.set_property_value("AcquisitionLoopTime", 42)

        # The saved configuration holds the tree below the instance along with
        # the property values set on it.
        configuration = device.save_configuration()
        print(f"Configuration length: {len(configuration)} characters")

        with open(CONFIG_FILE, "w") as file:
            file.write(configuration)
        print(f"Written to: {CONFIG_FILE}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
