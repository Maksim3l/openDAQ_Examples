##
# @tags: howto, properties, update
# @title: How to write several property values as one update
##
# Writes three property values between begin_update and end_update, showing
# that the values and the write notifications only land once the update ends.
##

import sys
import opendaq as daq


def on_write(sender, args):
    event_args = daq.IPropertyValueEventArgs.cast_from(args)
    print(f"  written: {event_args.property.name} = {event_args.value}")


if __name__ == "__main__":
    try:
        obj = daq.PropertyObject()
        obj.add_property(daq.FloatProperty("Gain", 1.0, True))
        obj.add_property(daq.IntProperty("BlockSize", 100, True))
        obj.add_property(daq.StringProperty("Label", "Channel", True))

        obj.on_any_property_value_write + daq.EventHandler(on_write)

        obj.begin_update()
        print(f"updating: {bool(obj.updating)}")

        obj.set_property_value("Gain", 4.0)
        obj.set_property_value("BlockSize", 512)
        obj.set_property_value("Label", "Pressure")

        # The writes are held until the update ends, so a read inside it still
        # returns the value the property had before.
        print(f"Gain inside the update: {obj.get_property_value('Gain')}")

        obj.end_update()
        print(f"updating: {bool(obj.updating)}")

        print()
        for prop in obj.visible_properties:
            print(f"{prop.name}: {obj.get_property_value(prop.name)}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
