# Copyright [2019] [Wojciech Wolny]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from ipaddress import IPv4Address, IPv4Network, ip_interface
from re import fullmatch
from typing import List, Union


def help():
    print('Script required two files with ips. Support only IPv4.\n'
          'Then will return groupd ip netwroks as subnets from first file \n'
          '\nFLAGS:\n'
          '\t--not-match: return list of not matched ip addresses \n'
          '\tOUTPUT: \n'
          '\t\t*-*-*-* Not matched *-*-*-*\n'
          '\t\t1 : 182.123.123.32 is host address\n'
          '\t\t2 : 55.54.53.0/30 is subnet\n'
          '\n\t--match: return grouped addresses \n'
          '\tOUTPUT: \n'
          '\t\t*-*-*-* 10.0.0.0/24 *-*-*-*\n'
          '\t\t1 : 10.0.0.1 is host address\n'
          '\t\t2 : 10.0.0.6 is host address\n'
          '\t\t3 : 10.0.0.8 is host address\n'
          '\t\t4 : 10.0.0.9 is host address\n'
          '\t\t5 : 10.0.0.4/30 is subnet\n'
          '\t\t*-*-*-* 192.168.2.0/24 *-*-*-*\n'
          '\n\t--not-empty: skip empty group networks\n'
          '\nEXAMPLE OF USE: \n'
          'Networsk file contain only list of networks and masks, separated by new line. \n'
          'Ipaddresses file contain only list of networks and masks or ip addresses, separated by new line.\n'
          '\n\t./network_recognision.py networks ipaddresses\n'
          '\nOUTPUT:\n'
          '\t*-*-*-* Not matched *-*-*-*\n'
          '\t1 : 182.123.123.32 is host address\n'
          '\t*-*-*-* 10.0.0.0/24 *-*-*-*\n'
          '\t1 : 10.0.0.1 is host address\n'
          '\t2 : 10.0.0.6 is host address\n'
          '\t3 : 10.0.0.8 is host address\n'
          '\t4 : 10.0.0.9 is host address\n'
          '\t5 : 10.0.0.4/30 is subnet\n'
          '\t*-*-*-* 192.168.2.0/24 *-*-*-*')


def read_file_to_list(file_name: str) -> list:
    with open(file_name) as source_file:
        output_list = [line.strip() for line in source_file.readlines()]
    return output_list


def create_list_of_subnets(list_of_ips: List[str]) -> List[Union[IPv4Address, IPv4Network]]:
    return [ip_interface(ip).network for ip in list_of_ips]


def create_list_of_networks(list_of_networks: List[str]) -> List[IPv4Network]:
    return [IPv4Network(network) for network in list_of_networks]


def compare_lists_of_addresses(subnet_list, network_list):
    result = {'Not matched': []}

    for subnet in subnet_list:
        match = False


        for network in network_list:
            if not str(network) in result:
                result[str(network)] = []

            if subnet.subnet_of(network):
                result[str(network)].append(str(subnet))
                match = True

        if not match:
            result['Not matched'].append(str(subnet))

    return result


def default_print(result):
    if '--not-match' in sys.argv:
        print(f'*-*-*-* Not matched *-*-*-*')
        i = 0
        for address, type in result['Not matched']:
            i += 1
            print(f'{i} : {address} is {type}')
    else:
        for key, values in result.items():
            if ('--match' in sys.argv and key == 'Not matched') or ('--not-empty' in sys.argv and values == []):
                continue
            print(f'*-*-*-* {key} *-*-*-*')
            i = 0
            for address in values:
                i += 1
                print(f'{i} : {address}')


if __name__ == '__main__':
    assert len(sys.argv) >= 3, 'script required to specify two source files'

    if '-h' in sys.argv or '--help' in sys.argv:
        help()
    else:
        network_file = sys.argv[1]
        network_list = read_file_to_list(network_file)
        network_list = create_list_of_networks(network_list)

        subnet_file = sys.argv[2]
        subnet_list = read_file_to_list(subnet_file)
        subnet_list = create_list_of_subnets(subnet_list)

        result = compare_lists_of_addresses(subnet_list, network_list)

        default_print(result)
