##
# @tags: howto, properties, selection
# @title: How to read and set a selection property
##
# Reads the value and the label of a selection property, changes the selection,
# and opens the input popup to pick a label.
##

import sys
import opendaq as daq
import Utils.daq_widget_util as daq_widget_util

if __name__ == "__main__":
    try:
        couplings = daq.List()
        for label in ("AC", "DC", "GND"):
            couplings.append(label)

        # A sparse selection carries its own integer keys instead of using
        # positions in a list.
        ranges = daq.Dict()
        ranges[1] = "1 V"
        ranges[10] = "10 V"
        ranges[100] = "100 V"

        obj = daq.PropertyObject()
        obj.add_property(daq.SelectionProperty("Coupling", couplings, 1, True))
        obj.add_property(daq.SparseSelectionProperty("Range", ranges, 10, True))

        # A list of labels is selected by position, a dict of labels by its own
        # keys, and the two report a different property type.
        for name in ("Coupling", "Range"):
            print(f"{name}: {obj.get_property(name).property_type}")

        # The property value is the key of the selected entry. The label it
        # stands for comes from get_property_selection_value.
        print()
        for name in ("Coupling", "Range"):
            print(f"{name}: key {obj.get_property_value(name)} "
                  f"= {obj.get_property_selection_value(name)}")

        obj.set_property_value("Coupling", 0)
        obj.set_property_value("Range", 100)

        print()
        for name in ("Coupling", "Range"):
            print(f"{name}: key {obj.get_property_value(name)} "
                  f"= {obj.get_property_selection_value(name)}")

        if "--widget" in sys.argv:
            daq_widget_util.make_widget(obj.get_property("Coupling"), obj)
            print()
            print(f"Coupling: key {obj.get_property_value('Coupling')} "
                  f"= {obj.get_property_selection_value('Coupling')}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
