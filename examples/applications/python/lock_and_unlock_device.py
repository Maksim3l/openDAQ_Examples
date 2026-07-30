##
# @tags: howto, device, lock
# @title: How to lock and unlock a device
##
# Locks a device, reads the lock state back, and unlocks it again.
##

import sys
import Utils.daq_utils as daq_utils

if __name__ == "__main__":
    try:
        device = daq_utils.setup_simulator()
        print(f"Device: {device.name}")
        print(f"Locked: {bool(device.locked)}")

        device.lock()
        print(f"Locked: {bool(device.locked)}")

        device.unlock()
        print(f"Locked: {bool(device.locked)}")

    except Exception as e:
        print(f"Example failed: {e}", file=sys.stderr)
        print("exit 1")
        sys.exit(1)

    print("exit 0")
    sys.exit(0)
