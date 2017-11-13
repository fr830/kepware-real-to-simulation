"""Turns live Kepware JSON file into simulation server"""
import json
from collections import OrderedDict
from lib.regular_register import RegularRegister
from lib.string_register import StringRegister
from lib.project import Project

def process_devices(devices, normal_register, string_register):
    """Process all tags in all devices"""
    for device in devices:
        for tag_group in device.tag_groups:
            for tag in tag_group.tags:
                if tag.data_type == 0: # string
                    tag.set_address(string_register.current_address)
                    string_register.move_to_next_address(2)
                elif tag.data_type == 1: # boolean
                    tag.set_address(normal_register.next_bit_address())
                    normal_register.move_to_next_bit_address()
                else: # integer
                    tag.set_address(normal_register.next_address())
                    normal_register.move_to_next_address(4)

def main():
    """MAIN"""
    with open("tags.json") as f_tags:
        text = f_tags.read().encode('utf_8')
        kepware_dict = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(text)
        project = Project(kepware_dict)
        for channel in project.channels:
            channel.set_driver_simulated()
            process_devices(channel.devices, RegularRegister(False), StringRegister(False))
        project.update()
        print project.as_json()

if __name__ == "__main__":
    main()
