##
# @tags: howto, properties, defaults
# @title: How to reset property values to their defaults
##
# Writes property values, clears one of them, and clears the rest, printing the
# values after each step.
##

import sys
import opendaq as daq


def print_values(obj, label):
    print(label)
    for prop in obj.visible_properties:
        print(f"  {prop.name}: {obj.get_property_value(prop.name)}"
              f" (default {prop.default_value})")


if __name__ == "__main__":
    try:
        obj = daq.PropertyObject()
        obj.add_property(daq.FloatProperty("Gain", 1.0, True))
        obj.add_property(daq.IntProperty("BlockSize", 100, True))
        obj.add_property(daq.StringProperty("Label", "Channel", True))

        obj.set_property_value("Gain", 4.0)
        obj.set_property_value("BlockSize", 512)
        obj.set_property_value("Label", "Pressure")
        print_values(obj, "After writing:")

        obj.clear_property_value("Gain")
        print()
        print_values(obj, "After clearing Gain:")

        obj.clear_property_values()
        print()
        print_values(obj, "After clearing every value:")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
