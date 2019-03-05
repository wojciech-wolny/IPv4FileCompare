# Copyright 2019 
# Wojciech Wolny & Ireneusz Wolny
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
from ipaddress import IPv4Network, ip_interface
from json import dumps
from typing import List, Dict, Generator, Union


class Config:
    json = '--json' in sys.argv
    match = '--match' in sys.argv
    not_match = '--not-match' in sys.argv
    not_empty = '--not-empty' in sys.argv

    file = any(['--file' in flag for flag in sys.argv])
    file_name = [flag.split('=')[1] for flag in sys.argv if '--file' in flag][0] if file else ''


def show_help_msg() -> None:
    print(
        'Script required two files with ips. Support only IPv4.\n'
        'Then will return groupd ip netwroks as subnets from first file \n'
        '\nFLAGS:\n'
        '\t-h --help: print help\n'
        '\t--not-match: return list of not matched ip addresses \n'
        '\tOUTPUT: \n'
        '\t\t*-*-*-* Not matched *-*-*-*\n'
        '\t\t1 : 182.123.123.32/32\n'
        '\t\t2 : 55.54.53.0/30 \n'
        '\n\t--match: return grouped addresses \n'
        '\tOUTPUT: \n'
        '\t\t*-*-*-* 10.0.0.0/24 *-*-*-*\n'
        '\t\t1 : 10.0.0.1/32 \n'
        '\t\t2 : 10.0.0.6/32 \n'
        '\t\t3 : 10.0.0.8/32 \n'
        '\t\t4 : 10.0.0.9/32 \n'
        '\t\t5 : 10.0.0.4/30 \n'
        '\t\t*-*-*-* 192.168.2.0/24 *-*-*-*\n'
        '\n\t--not-empty: skip empty group networks\n'
        '\n\t--json: return json representation of results\n'
        '\n\t--file={file_name}: print results to file with given name, don\'t overwrite file if exists\n'
        '\nEXAMPLE OF USE: \n'
        'Networsk file contain only list of networks and masks, separated by new line. \n'
        'Ipaddresses file contain only list of networks and masks or ip addresses, separated by new line.\n'
        '\n\t./network_recognision.py networks ipaddresses\n'
        '\nOUTPUT:\n'
        '\t*-*-*-* Not matched *-*-*-*\n'
        '\t1 : 182.123.123.32 \n'
        '\t*-*-*-* 10.0.0.0/24 *-*-*-*\n'
        '\t1 : 10.0.0.1/32 \n'
        '\t2 : 10.0.0.6/32 \n'
        '\t3 : 10.0.0.8/32 \n'
        '\t4 : 10.0.0.9/32 \n'
        '\t5 : 10.0.0.4/30 \n'
        '\t*-*-*-* 192.168.2.0/24 *-*-*-*'
    )


def read_file_to_list(file_name: str) -> list:
    with open(file_name) as source_file:
        output_list = [line.strip() for line in source_file.readlines()]
    return output_list


def create_list_of_subnets(list_of_ips: List[str]) -> List[IPv4Network]:
    return [ip_interface(ip).network for ip in list_of_ips]


def create_list_of_networks(list_of_networks: List[str]) -> List[IPv4Network]:
    return [IPv4Network(network) for network in list_of_networks]


def compare_lists_of_addresses(subnet_list: List[IPv4Network], network_list: List[IPv4Network]) -> Dict:
    results = {'NotMatched': []}

    for subnet in subnet_list:
        match = False

        for network in network_list:
            if not str(network) in results:
                results[str(network)] = []

            if subnet.subnet_of(network):
                results[str(network)].append(str(subnet))
                match = True

        if not match:
            results['NotMatched'].append(str(subnet))

    return results


def prepare_default_print(result: Dict) -> Generator:
    if Config.not_match:
        yield f'*-*-*-* Not matched *-*-*-*'
        i = 0
        for address in result['NotMatched']:
            i += 1
            yield f'{i} : {address}'
    else:
        for key, values in result.items():
            if (Config.match and key == 'NotMatched') or (Config.not_empty and values == []):
                continue
            elif key == 'NotMatched':
                key = 'Not matched'
            yield f'*-*-*-* {key} *-*-*-*'
            i = 0
            for address in values:
                i += 1
                yield f'{i} : {address}'


def print_results(results: Union[Dict, str]) -> None:
    if Config.file:
        with open(Config.file_name, 'a') as output_file:
            if Config.json:
                output_file.write(f'{dumps(results)}\n')
            else:
                for line in prepare_default_print(results):
                    output_file.write(f'{line}\n')
    else:
        if Config.json:
            print(dumps(results))
        else:
            for line in prepare_default_print(results):
                print(line)


def run() -> None:
    network_file = sys.argv[1]
    network_list = read_file_to_list(network_file)
    network_list = create_list_of_networks(network_list)

    subnet_file = sys.argv[2]
    subnet_list = read_file_to_list(subnet_file)
    subnet_list = create_list_of_subnets(subnet_list)

    results = compare_lists_of_addresses(subnet_list, network_list)

    print_results(results)


if __name__ == '__main__':
    assert len(sys.argv) >= 3, 'script required to specify two source files'

    if '-h' in sys.argv or '--help' in sys.argv:
        show_help_msg()
    else:
        run()
