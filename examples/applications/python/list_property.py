##
# @tags: howto, properties, list
# @title: How to read and modify a list property
##
# Reads a list property, writes a longer list back, and opens the input popup
# to edit the items.
##

import sys
import opendaq as daq
import Utils.daq_widget_util as daq_widget_util

if __name__ == "__main__":
    try:
        thresholds = daq.List()
        for value in (1.0, 2.5, 5.0):
            thresholds.append(value)

        obj = daq.PropertyObject()
        obj.add_property(daq.ListProperty("Thresholds", thresholds, True))

        prop = obj.get_property("Thresholds")
        print(f"Item type: {prop.item_type}")

        values = obj.get_property_value("Thresholds")
        for value in values:
            print(f"  {value}")

        # The property takes the whole list as its value.
        updated = daq.List()
        for value in values:
            updated.append(value)
        updated.append(7.5)
        obj.set_property_value("Thresholds", updated)

        print()
        for value in obj.get_property_value("Thresholds"):
            print(f"  {value}")

        if "--widget" in sys.argv:
            written = daq_widget_util.make_widget(prop, obj)
            if written is not None:
                print()
                for value in written:
                    print(f"  {value}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
