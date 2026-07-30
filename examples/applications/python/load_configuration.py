##
# @tags: howto, save-load
# @title: How to load a configuration
##
# Saves a configuration, changes the property it recorded, then loads the
# configuration back and reads the property again.
##

import sys
import Utils.daq_utils as daq_utils

PROPERTY = "AcquisitionLoopTime"

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()

        device.set_property_value(PROPERTY, 42)
        configuration = device.save_configuration()
        print(f"Saved with {PROPERTY} = {device.get_property_value(PROPERTY)}")

        device.set_property_value(PROPERTY, 20)
        print(f"Changed to {PROPERTY} = {device.get_property_value(PROPERTY)}")

        device.load_configuration(configuration)
        print(f"Loaded, {PROPERTY} = {device.get_property_value(PROPERTY)}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
