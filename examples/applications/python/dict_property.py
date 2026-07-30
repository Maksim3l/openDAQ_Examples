##
# @tags: howto, properties, dict
# @title: How to read and modify a dict property
##
# Reads a dict property, writes an extra entry back, and opens the input popup
# to edit the entries.
##

import sys
import opendaq as daq
import Utils.daq_widget_util as daq_widget_util

if __name__ == "__main__":
    try:
        channel_names = daq.Dict()
        channel_names[1] = "Pressure"
        channel_names[2] = "Temperature"

        obj = daq.PropertyObject()
        obj.add_property(daq.DictProperty("ChannelNames", channel_names, True))

        prop = obj.get_property("ChannelNames")
        print(f"Key type:  {prop.key_type}")
        print(f"Item type: {prop.item_type}")

        entries = obj.get_property_value("ChannelNames")
        for key, value in entries.items():
            print(f"  {key}: {value}")

        # The property takes the whole dict as its value.
        updated = daq.Dict()
        for key, value in entries.items():
            updated[key] = value
        updated[3] = "Strain"
        obj.set_property_value("ChannelNames", updated)

        print()
        for key, value in obj.get_property_value("ChannelNames").items():
            print(f"  {key}: {value}")

        if "--widget" in sys.argv:
            written = daq_widget_util.make_widget(prop, obj)
            if written is not None:
                print()
                for key, value in written.items():
                    print(f"  {key}: {value}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
