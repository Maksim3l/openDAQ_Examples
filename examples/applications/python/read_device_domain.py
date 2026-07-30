##
# @tags: howto, device, domain
# @title: How to read a device's domain
##
# Prints the device's tick resolution, origin and domain unit, then converts its
# current tick count into seconds since that origin.
##

import sys
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()
        domain = device.domain

        resolution = domain.tick_resolution
        print(f"Device: {device.name}")
        print(f"Tick resolution: {resolution.numerator}/{resolution.denominator}")
        print(f"Origin:          {domain.origin}")
        print(f"Unit:            {domain.unit.symbol} ({domain.unit.name})")

        ticks = device.ticks_since_origin
        seconds = ticks * resolution.numerator / resolution.denominator
        print(f"\nTicks since origin: {ticks}")
        print(f"Seconds since origin: {seconds:.6f}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
