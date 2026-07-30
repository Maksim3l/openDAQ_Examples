##
# Tkinter input popup for a single property whose value cannot be shown or
# collected on the console: selections, enumerations, lists, dicts, structs,
# nested objects and callable properties.
#
# An example does its own openDAQ work and calls make_widget() only to show a
# value or to collect one. Everything the popup writes goes through
# set_property_value, so an example that never opens the popup behaves the same.
##

import tkinter as tk
from tkinter import ttk

import opendaq as daq

SELECTION_TYPES = (daq.PropertyType.Selection,
                   daq.PropertyType.IndexSelection,
                   daq.PropertyType.SparseSelection)
METHOD_TYPES = (daq.PropertyType.Function, daq.PropertyType.Procedure)
TEXT_TYPES = (daq.PropertyType.Int, daq.PropertyType.Float,
              daq.PropertyType.String)
CONTAINER_TYPES = (daq.PropertyType.List, daq.PropertyType.Dict)


# A reference property reports the type of the property it currently points to.
def property_type_of(prop):
    if prop.property_type == daq.PropertyType.Reference:
        return prop.referenced_property.property_type
    return prop.property_type


# The name of the enumerator the value holds. Enumerator values are free to
# start anywhere, so the name list must not be indexed with the integer value.
def enumerator_name(value):
    for name, int_value in value.enumeration_type.as_dictionary.items():
        if int(int_value) == int(value.value):
            return str(name)
    return str(value)


def _coerce(core_type, text):
    if core_type == daq.CoreType.ctInt:
        return int(text)
    if core_type == daq.CoreType.ctFloat:
        return float(text)
    if core_type == daq.CoreType.ctBool:
        return text.strip().lower() in ('1', 'true', 'yes')
    return text


# Selection values are a list indexed by position, or a dict keyed by the
# integer the property value takes. Both are written back as that integer.
def _selection_entries(prop):
    values = prop.selection_values
    entries = []
    if daq.IDict.can_cast_from(values):
        for key, label in daq.IDict.cast_from(values).items():
            entries.append((int(key), str(label)))
    else:
        index = 0
        for label in daq.IList.cast_from(values):
            entries.append((index, str(label)))
            index += 1
    return entries


class _Row:
    def __init__(self, prop):
        self.prop = prop
        self.name = prop.name

    def build(self, parent):
        raise NotImplementedError

    # The value to write, or None when the row holds nothing to write.
    def value(self):
        return None


class _BoolRow(_Row):
    def build(self, parent):
        self.var = tk.BooleanVar(value=bool(self.prop.value))
        return ttk.Checkbutton(parent, variable=self.var)

    def value(self):
        return self.var.get()


class _TextRow(_Row):
    def build(self, parent):
        self.var = tk.StringVar(value=str(self.prop.value))
        suggested = self.prop.suggested_values
        if suggested is not None and len(suggested):
            labels = []
            for item in suggested:
                labels.append(str(item))
            return ttk.Combobox(parent, textvariable=self.var, values=labels)
        return ttk.Entry(parent, textvariable=self.var)

    def value(self):
        return _coerce(self.prop.value_type, self.var.get())


class _SelectionRow(_Row):
    def build(self, parent):
        self.entries = _selection_entries(self.prop)
        labels = []
        for _, label in self.entries:
            labels.append(label)
        self.var = tk.StringVar()
        combobox = ttk.Combobox(parent, textvariable=self.var,
                                values=labels, state='readonly')
        current = int(self.prop.value)
        for key, label in self.entries:
            if key == current:
                self.var.set(label)
        return combobox

    def value(self):
        for key, label in self.entries:
            if label == self.var.get():
                return key
        return None


class _EnumerationRow(_Row):
    def build(self, parent):
        self.enum_type = self.prop.value.enumeration_type
        names = []
        for name in self.enum_type.enumerator_names:
            names.append(str(name))
        self.var = tk.StringVar(value=enumerator_name(self.prop.value))
        return ttk.Combobox(parent, textvariable=self.var,
                            values=names, state='readonly')

    def value(self):
        return daq.EnumerationWithType(
            self.enum_type, daq.String(self.var.get()))


# List items one per line, dict entries as "key = value" one per line.
class _ContainerRow(_Row):
    def build(self, parent):
        self.is_dict = property_type_of(self.prop) == daq.PropertyType.Dict
        lines = []
        if self.is_dict:
            for key, item in self.prop.value.items():
                lines.append(f'{key} = {item}')
        else:
            for item in self.prop.value:
                lines.append(str(item))

        self.text = tk.Text(parent, height=min(6, max(2, len(lines))), width=40)
        self.text.insert('1.0', '\n'.join(lines))
        return self.text

    def value(self):
        item_type = self.prop.item_type
        if self.is_dict:
            key_type = self.prop.key_type
            result = daq.Dict()
            for line in self.text.get('1.0', tk.END).splitlines():
                if not line.strip():
                    continue
                key, _, item = line.partition('=')
                result[_coerce(key_type, key.strip())] = _coerce(
                    item_type, item.strip())
            return result

        result = daq.List()
        for line in self.text.get('1.0', tk.END).splitlines():
            if not line.strip():
                continue
            result.append(_coerce(item_type, line.strip()))
        return result


class _StructRow(_Row):
    def build(self, parent):
        struct = self.prop.value
        names = struct.struct_type.field_names
        values = struct.field_values
        frame = ttk.Frame(parent)
        for i in range(0, len(names)):
            ttk.Label(frame, text=f'{names[i]}: {values[i]}').pack(anchor=tk.W)
        return frame


class _ObjectRow(_Row):
    def build(self, parent):
        frame = ttk.Frame(parent)
        for prop in self.prop.value.visible_properties:
            ttk.Label(frame, text=f'{prop.name}: {prop.value}').pack(anchor=tk.W)
        return frame


class _MethodRow(_Row):
    def build(self, parent):
        frame = ttk.Frame(parent)
        self.result = ttk.Label(frame, text='')
        self.entries = []

        # Argument info is a struct, so it needs a cast to be read by name.
        for argument in self.prop.callable_info.arguments:
            info = daq.IArgumentInfo.cast_from(argument)
            ttk.Label(frame, text=str(info.name)).pack(side=tk.LEFT)
            var = tk.StringVar()
            ttk.Entry(frame, textvariable=var, width=8).pack(side=tk.LEFT)
            self.entries.append((info.type, var))

        ttk.Button(frame, text='Call', command=self._call).pack(side=tk.LEFT)
        self.result.pack(side=tk.LEFT, padx=6)
        return frame

    def _call(self):
        is_function = property_type_of(self.prop) == daq.PropertyType.Function
        callable_class = daq.IFunction if is_function else daq.IProcedure
        method = callable_class.cast_from(self.prop.value)

        arguments = []
        for core_type, var in self.entries:
            arguments.append(_coerce(core_type, var.get()))

        returned = method(*arguments)
        self.result.configure(text=str(returned) if is_function else 'called')


_ROW_TYPES = {
    daq.PropertyType.Bool: _BoolRow,
    daq.PropertyType.Int: _TextRow,
    daq.PropertyType.Float: _TextRow,
    daq.PropertyType.String: _TextRow,
    daq.PropertyType.Enumeration: _EnumerationRow,
    daq.PropertyType.List: _ContainerRow,
    daq.PropertyType.Dict: _ContainerRow,
    daq.PropertyType.Struct: _StructRow,
    daq.PropertyType.Object: _ObjectRow,
}


def _row_for(prop):
    property_type = property_type_of(prop)
    if property_type in SELECTION_TYPES:
        return _SelectionRow(prop)
    if property_type in METHOD_TYPES:
        return _MethodRow(prop)
    return _ROW_TYPES[property_type](prop)


##
# Opens a modal popup holding the input control that suits the property's type,
# and writes the value confirmed with Set back through set_property_value.
# Returns the value written, or None if the popup was closed without one.
##
def make_widget(prop, obj):
    row = _row_for(prop)
    written = []

    root = tk.Tk()
    root.title(prop.name)

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text=prop.name).grid(
        row=0, column=0, sticky=tk.NW, padx=(0, 8), pady=3)
    row.build(frame).grid(row=0, column=1, sticky=tk.W, pady=3)

    def on_set():
        value = row.value()
        if value is not None and not prop.read_only:
            obj.set_property_value(prop.name, value)
            written.append(obj.get_property_value(prop.name))
        root.destroy()

    buttons = ttk.Frame(frame, padding=(0, 10, 0, 0))
    buttons.grid(row=1, column=0, columnspan=2, sticky=tk.E)
    ttk.Button(buttons, text='Set', command=on_set).pack(side=tk.LEFT, padx=4)
    ttk.Button(buttons, text='Close', command=root.destroy).pack(side=tk.LEFT)

    root.mainloop()
    return written[0] if written else None
