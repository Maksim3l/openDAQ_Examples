##
# @tags: tutorial, quickstart
# @title: openDAQ Python Quickstart
##
# This walkthrough covers the fundamentals of working with openDAQ in
# Python. It goes from creating an instance to reading processed data
# from a function block, one step at a time.
#
# Each section builds on the previous one. By the end you'll have:
# - Created an openDAQ instance
# - Discovered and connected to a simulator device
# - Explored the device's component tree
# - Peeked at live data with signal.last_value
# - Read signal data with a StreamReader
# - Inspected domain descriptors and read timestamps
# - Added a function block and connected signals
# - Discovered and changed properties
# - Modulated a property in real time and observed the effect
##

import sys
sys.path.append("..")
import time
import opendaq as daq
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        # ─── Step 1: Create an instance ───────────────────────────
        #
        # The Instance is the entry point to everything in openDAQ.
        # It manages modules, devices, function blocks, and servers.
        # Creating one loads all available modules from the default
        # module path.

        instance = daq.Instance()
        print("Instance created")
        print(f"  Available device types: {len(instance.available_device_types)}")
        print(f"  Available FB types: {len(instance.available_function_block_types)}")

        # ─── Step 2: Set up and connect to a device ───────────────
        #
        # In a real application you'd discover devices on the network
        # with instance.available_devices and connect to one. Here we
        # set up a local simulator so this script works standalone.
        #
        # The simulator is a reference device that generates sine wave
        # signals, has configurable channels, and behaves like a real
        # DAQ device.

        simulator = daq_utils.setup_simulator()
        device = daq_utils.add_simulator(instance)
        print(f"\nConnected to: {device.name}")
        print(f"  Serial number: {device.info.serial_number}")
        print(f"  Model: {device.info.model}")

        # ─── Step 3: Explore the device tree ──────────────────────
        #
        # Every device is a tree of components. At the top level you
        # find channels, signals, function blocks, and sub-devices.
        # Channels are where physical (or simulated) data comes from.
        # Signals carry that data to wherever it's needed.

        channels = device.channels
        signals = device.get_signals_recursive()
        print(f"\nDevice tree:")
        print(f"  Channels: {len(channels)}")
        print(f"  Signals (recursive): {len(signals)}")

        for ch in channels:
            print(f"  Channel: {ch.name} ({ch.global_id})")

        # Grab a signal we'll use for the rest of the walkthrough.
        # Any value signal works; we just need one that's producing data.
        signal = channels[0].signals[0]
        print(f"\nUsing signal: {signal.name}")

        # ─── Step 4: Peek at data with last_value ─────────────────
        #
        # The simplest way to see what a signal is doing right now.
        # last_value returns the most recent sample without creating
        # a reader or worrying about buffers. Good for dashboards
        # and quick checks.

        time.sleep(0.1)
        print(f"\nLast value: {signal.last_value}")

        # ─── Step 5: Read signal data with a StreamReader ─────────
        #
        # For continuous data, create a StreamReader. It buffers
        # incoming samples so you can read them in batches. Every
        # call to read() returns whatever arrived since the last call.
        #
        # The value_type parameter tells the reader what numeric type
        # you want the samples in. Float64 is the safest default.

        reader = daq.StreamReader(signal, value_type=daq.SampleType.Float64)
        time.sleep(0.1)

        values = reader.read(100)
        print(f"\nStreamReader got {len(values)} samples:")
        for i, v in enumerate(values[:5]):
            print(f"  [{i}] {v:.4f}")
        if len(values) > 5:
            print(f"  ... ({len(values) - 5} more)")

        # ─── Step 6: Understand the time domain ───────────────────
        #
        # Every value signal has a domain signal (usually time) that
        # tells you when each sample was taken. The domain signal's
        # descriptor holds the resolution, origin, and unit you need
        # to convert raw ticks into real-world timestamps.

        domain_descriptor = signal.domain_signal.descriptor
        resolution = domain_descriptor.tick_resolution
        origin = domain_descriptor.origin
        unit_symbol = domain_descriptor.unit.symbol

        print(f"\nDomain info:")
        print(f"  Resolution: {resolution}")
        print(f"  Origin: {origin}")
        print(f"  Unit: {unit_symbol}")

        # read_with_domain gives you both value samples and their
        # corresponding domain (tick) values. Multiply ticks by the
        # resolution to get seconds.
        time.sleep(0.1)
        samples, domain_samples = reader.read_with_domain(100)
        if len(samples) > 0:
            domain_seconds = domain_samples * float(resolution)
            print(f"\nWith domain (manual scaling):")
            for i in range(min(3, len(samples))):
                print(f"  Value: {samples[i]:.4f}, Time: {domain_seconds[i]:.6f} {unit_symbol}")

        # ─── Step 7: Read with human-readable timestamps ──────────
        #
        # TimeStreamReader wraps a regular reader and converts domain
        # ticks to datetime objects. This is the easiest way to get
        # timestamps without doing the math yourself.

        time_reader = daq.TimeStreamReader(reader)
        time.sleep(0.1)

        samples, timestamps = time_reader.read_with_timestamps(100)
        if len(samples) > 0:
            print(f"\nWith timestamps (TimeStreamReader):")
            for i in range(min(3, len(samples))):
                print(f"  Value: {samples[i]:.4f}, Time: {timestamps[i]}")

        # ─── Step 8: Add a function block ─────────────────────────
        #
        # Function blocks process signal data. A statistics FB
        # computes mean, RMS, and min/max over a sliding window.
        # You connect a signal to its input port, and it produces
        # new output signals with the computed values.

        statistics = instance.add_function_block("RefFBModuleStatistics")
        print(f"\nAdded function block: {statistics.name}")

        input_port = statistics.input_ports[0]
        input_port.connect(signal)
        print(f"  Connected {signal.name} -> {input_port.name}")

        fb_signals = statistics.get_signals_recursive()
        print(f"  Output signals: {len(fb_signals)}")
        for s in fb_signals:
            print(f"    {s.name}")

        # ─── Step 9: Discover and change properties ───────────────
        #
        # Every component has properties that control its behavior.
        # Before changing anything, you can list what's available.
        # Visible properties are the ones meant for users; read_only
        # ones can't be changed from application code.

        channel = channels[0]
        print(f"\nProperties on {channel.name}:")
        for prop in channel.visible_properties:
            ro = " (read-only)" if prop.read_only else ""
            print(f"  {prop.name}: {channel.get_property_value(prop.name)}{ro}")

        # Change the signal frequency
        print(f"\nFrequency before: {channel.get_property_value('Frequency')}")
        channel.set_property_value("Frequency", 5)
        print(f"Frequency after:  {channel.get_property_value('Frequency')}")

        # ─── Step 10: Live property modulation ────────────────────
        #
        # Properties take effect immediately. Here we ramp the
        # amplitude up and down while reading the statistics FB's
        # output, showing that property changes flow through the
        # entire signal chain in real time.

        channel.set_property_value("NoiseAmplitude", 0.75)
        fb_reader = daq.StreamReader(fb_signals[0], value_type=daq.SampleType.Float64)
        time.sleep(0.2)

        amplitude_step = 0.5
        print(f"\nModulating amplitude for 2 seconds...")
        for i in range(40):
            time.sleep(0.05)
            amplitude = channel.get_property_value("Amplitude")
            if not (1.5 <= amplitude <= 9.5):
                amplitude_step = -amplitude_step
            channel.set_property_value("Amplitude", amplitude + amplitude_step)

            fb_values = fb_reader.read(100)
            if len(fb_values) > 0:
                print(f"  Amplitude: {amplitude:5.1f}  |  Stats output: {fb_values[-1]:.4f}")

        print("\nDone. You've created an instance, connected to a device,")
        print("read raw and timestamped data, added processing with a")
        print("function block, and modulated properties in real time.")

    except Exception as e:
        print(f"Quickstart failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)