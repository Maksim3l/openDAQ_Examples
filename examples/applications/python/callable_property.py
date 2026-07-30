##
# @tags: howto, properties, callable
# @title: How to call a function or procedure property
##
# Adds a function property and a procedure property, calls both, and opens the
# input popup to call the function with arguments typed in.
##

import os
import sys
import opendaq as daq
import Utils.daq_widget_util as daq_widget_util


def scale(value, factor):
    return value * factor


def reset():
    print("  reset called")


if __name__ == "__main__":
    try:
        obj = daq.PropertyObject()

        # ctUndefined as the callable info's return type makes a procedure
        # property, any other type makes a function property.
        scale_info = daq.CallableInfo(
            [daq.ArgumentInfo("value", daq.CoreType.ctFloat),
             daq.ArgumentInfo("factor", daq.CoreType.ctFloat)],
            daq.CoreType.ctFloat, False)
        reset_info = daq.CallableInfo([], daq.CoreType.ctUndefined, False)

        obj.add_property(daq.FunctionProperty("Scale", scale_info, True))
        obj.add_property(daq.FunctionProperty("Reset", reset_info, True))

        obj.set_property_value("Scale", daq.Function(scale))
        obj.set_property_value("Reset", daq.Procedure(reset))

        for name in ("Scale", "Reset"):
            print(f"{name}: {obj.get_property(name).property_type}")

        scale_method = daq.IFunction.cast_from(obj.get_property_value("Scale"))
        print(f"\nScale(2.5, 4.0) = {scale_method(2.5, 4.0)}")

        reset_method = daq.IProcedure.cast_from(obj.get_property_value("Reset"))
        reset_method()

        if "--widget" in sys.argv:
            daq_widget_util.make_widget(obj.get_property("Scale"), obj)

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    # A function property that has been called takes the interpreter down with
    # it on shutdown, so exit immediately instead of returning through it.
    print("exit 0")
    sys.stdout.flush()
    os._exit(0)
