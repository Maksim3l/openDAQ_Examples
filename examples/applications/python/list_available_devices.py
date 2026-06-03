##
# Discovers and connects to both remote and local devices. The default openDAQ installation
# bundle contains a simulator and an audio device module that allow us to instantiate local
# devices. Those will appear during discovery as devices with connection strings prefixed
# with "daqref" and "miniaudio".
#
# Remote devices are those that are running their own openDAQ instance with a server. To
# a simulator of such a device, the example in "Integration Examples/simulator.py" can be
# used.
##

import opendaq as daq
import sys
sys.path.append("..")
import daq_utils

if __name__ == "__main__":
    instance = daq.Instance()

    remote_device_info = []
    local_device_info = []
    available_devices = instance.available_devices

    # Device info contains basic device information, as well as all required information to
    # connect to the device.
    for device_info in available_devices:
        if len(device_info.server_capabilities):
            remote_device_info.append(device_info)
        else:
            local_device_info.append(device_info)

    connection_strings = []
    print('\nRemote discovered devices:')
    for device_info in remote_device_info:
        print('\n' + device_info.name + ':')
        daq_utils.print_property_object(device_info, 1)
        connection_strings.append(device_info.connection_string)

    print('\nLocal discovered devices:')
    for device_info in local_device_info:
        print('\n' + device_info.name + ':')
        daq_utils.print_property_object(device_info, 1)
        connection_strings.append(device_info.connection_string)
