##
# @tags: howto, properties, nested
# @title: How to read and write properties on a nested property object
##
# Adds an object property, reads and writes the properties inside it through a
# dotted path and through the nested object itself, and opens the input popup
# to show its contents.
##

import sys
import opendaq as daq
import Utils.daq_widget_util as daq_widget_util

if __name__ == "__main__":
    try:
        filter_settings = daq.PropertyObject()
        filter_settings.add_property(daq.FloatProperty("Cutoff", 1000.0, True))
        filter_settings.add_property(daq.IntProperty("Order", 2, True))

        obj = daq.PropertyObject()
        obj.add_property(daq.ObjectProperty("Filter", filter_settings))

        # A dotted path reaches into the nested object from the owner.
        print(f"Filter.Cutoff: {obj.get_property_value('Filter.Cutoff')}")
        print(f"Filter.Order:  {obj.get_property_value('Filter.Order')}")

        obj.set_property_value("Filter.Cutoff", 250.0)

        # The nested object can also be read out and used on its own.
        nested = obj.get_property_value("Filter")
        nested.set_property_value("Order", 4)

        print()
        for prop in nested.visible_properties:
            print(f"{prop.name}: {nested.get_property_value(prop.name)}")

        if "--widget" in sys.argv:
            daq_widget_util.make_widget(obj.get_property("Filter"), obj)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
