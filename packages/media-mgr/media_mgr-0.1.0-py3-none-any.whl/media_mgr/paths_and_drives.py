#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Path and Drive Handling
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from collections import defaultdict

import getpass
import subprocess
import re
import json

from quickcolor.color_def import color
from delayviewer.spinner import Spinner, handle_spinner
from delayviewer.time_and_delay import time_show

from .comms_utility import run_cmd, is_server_active
from .media_cfg import MediaConfig

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_drive_stats(ipv4: str | None = None):
    driveStats = defaultdict(list)
    # returns value is a list of strings (ie: CRLF separated lines)
    allDriveStats = run_cmd(ipv4, "df -h | grep 'sd[b-z]' | sort -k 6")
    if allDriveStats == [''] or ('returncode' in allDriveStats and allDriveStats.returncode != 0):
        raise BlockingIOError(f'Warning: Could not retrieve drive paths from IPV4 {ipv4}!')

    for driveInfo in allDriveStats:
        # separate string into list of ascii fields separated by white space
        driveItems = re.sub(' +', ' ', driveInfo).split(' ')

        # allocate indexed item components into dictionary of lists
        # each list contains type specific contents
        driveStats['size'].append(driveItems[1])
        driveStats['used'].append(driveItems[2])
        driveStats['avail'].append(driveItems[3])
        driveStats['percent'].append(driveItems[4])
        driveStats['path'].append(driveItems[5])

    return driveStats

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

@time_show
def show_drive_info(ipv4: str | None = None):
    driveStats = get_drive_stats(ipv4)

    print(f'\n{color.CBLUE2}Drive Info     - {color.CBLUE}{ipv4 if ipv4 else "Local"}')
    print(f'{color.CWHITE}----- ----')

    for idx, zipItems in enumerate(zip(driveStats['size'], driveStats['used'],
        driveStats['avail'], driveStats['percent'], driveStats['path'])):
        size, used, avail, percent, path = zipItems
        print(f'{color.CGREEN}{idx+1:>3}. {path:<40} {color.CYELLOW} ' + \
                f'{size:<5} {used:<5} {avail:<5} {color.CCYAN}' + \
                f'{percent:>5}{color.CEND}')

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_drive_paths(ipv4: str | None = None, serverType: str = 'plex'):
    if serverType != 'plex':
        return [ run_cmd(ipv4, "pwd")[0] + "/Desktop/Loris-Lots" ]

    cmdResult = run_cmd(ipv4, "df -h | grep 'sd[b-z]' | sort -k 6 | awk '{ print $6 }'")
    if type(cmdResult) is subprocess.CompletedProcess and cmdResult.returncode != 0:
        raise BlockingIOError(f"Warning: Could not retrieve drive paths from IPV4 {ipv4}!")

    return cmdResult

# ------------------------------------------------------------------------------------------------------

def create_full_search_path_list_for_drive(drivePath: str):
    mc = MediaConfig()
    searchNameList = mc.get_configured_entries()

    fullSearchPathListForDrive = []
    for searchName in searchNameList:
        fullSearchPathListForDrive.append(f'{drivePath}/{searchName}')

    return fullSearchPathListForDrive

# ------------------------------------------------------------------------------------------------------

def get_full_search_paths_all_drives(ipv4: str | None = None, serverType: str = 'plex'):
    '''
    For Plex servers, merge all discovered drive mount paths with possible media sub-paths
    Media sub-paths are specified in pathNames.json in the personal cfg dir
    These are potential paths configured, not necessarily paths that exist
    The filtering method below is intended to filter out what does not exist
    as well as specific paths that exist but that are not part of config!
    '''
    drivePaths = get_drive_paths(ipv4, serverType)

    fullSearchPathsAllDrives = []

    if serverType == 'plex':
        for drivePath in drivePaths:
            searchPathListForDrive = create_full_search_path_list_for_drive(drivePath)
            fullSearchPathsAllDrives += searchPathListForDrive

    elif serverType == 'worker':
        fullSearchPathsAllDrives = get_all_media_paths(ipv4, serverType)

    return sorted(fullSearchPathsAllDrives)

# ------------------------------------------------------------------------------------------------------

def get_all_media_paths(ipv4: str | None = None, serverType: str = 'plex'):
    '''
    For Plex servers, retrieve all existing drive mounts with media sub-paths that actually exist
    in the file system
    '''
    paths = run_cmd(ipv4, f'ls -d /media/{getpass.getuser()}/*/*') if serverType == 'plex' else \
            run_cmd(ipv4, f'ls -d /home/{getpass.getuser()}/Desktop/Loris-Lots/* | grep Incoming')

    if type(paths) is subprocess.CompletedProcess:
        raise BlockingIOError(f"Warning: Could not retrieve drive paths from IPV4 {ipv4}!")

    return sorted(paths)

# ------------------------------------------------------------------------------------------------------

def get_filtered_media_paths(ipv4: str | None = None, serverType: str = 'plex'):
    '''
    Taking all media paths that exist (drive mount paths plus media sub paths) and filter against
    all possible search paths on all mount paths - subset represents searchable paths that exist
    in the file system and that are part of the configured pathNames.json group
    '''
    paths = get_all_media_paths(ipv4, serverType)
    fullPaths = get_full_search_paths_all_drives(ipv4, serverType)

    return sorted(list(set(paths).intersection(fullPaths)))

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_lsblk_devices_and_mounts(ipv4: str | None = None):
    cmdResult = run_cmd(ipv4, "lsblk -b --json", jsonOutput=True)
    # cmdResult = run_cmd(ipv4, "lsblk -b | grep 'sd[b-z]' | grep 'part|disk' | awk '{ print $1, $4, $7 }'")
    if type(cmdResult) is subprocess.CompletedProcess:
        raise BlockingIOError(f"Warning: Could not retrieve devices and mount paths from IPV4 {ipv4}!")

    # print(json.dumps(cmdResult, indent=4))
    mountableDevices = []
    for dev in cmdResult['blockdevices']:
        if re.match("sd[b-z]", dev['name']):
            mountableDevices.append(dev)

    return mountableDevices

# ------------------------------------------------------------------------------------------------------

def get_lsblk_mountable_partitions(ipv4: str | None = None):
    mountableDevices = get_lsblk_devices_and_mounts(ipv4=ipv4)
    mountablePartitions = []
    for dev in mountableDevices:
        for child in dev['children']:
            if child['size'] > 1_000_000_000:
                mountablePartitions.append(child)

    return mountablePartitions

# ------------------------------------------------------------------------------------------------------

def show_dev_partitions(ipv4: str | None = None,
        partitionsThatAreAlreadyMounted: list | None = None,
        partitionsThatAreUnmounted : list | None = None):
    availablePartitions = []
    if not partitionsThatAreAlreadyMounted:
        availablePartitions = get_lsblk_mountable_partitions(ipv4=ipv4)
        partitionsThatAreAlreadyMounted = [ x for x in availablePartitions if x['mountpoints'] != [ None ] ]

    if not partitionsThatAreUnmounted:
        if not availablePartitions:
            availablePartitions = get_lsblk_mountable_partitions(ipv4=ipv4)
        partitionsThatAreUnmounted = [ x for x in availablePartitions if x['mountpoints'] == [ None ] ]

    if partitionsThatAreAlreadyMounted:
        print(f'\n{color.CBLUE2}-- The following {color.CWHITE}{len(partitionsThatAreAlreadyMounted)}' + \
                f'{color.CBLUE2} devices on {color.CWHITE}{ipv4}{color.CBLUE2} are mounted!{color.CEND}\n')
        for idx, partition in enumerate(partitionsThatAreAlreadyMounted):
            print(f'   {color.CGREEN2}{idx+1:>3}. {color.CEND}Device ' + \
                    f'{color.CCYAN}/dev/{partition["name"]}{color.CEND} ' + \
                    f'mount point is {color.CYELLOW}{partition["mountpoints"][0]}{color.CEND}')

    if partitionsThatAreUnmounted:
        print(f'\n{color.CBLUE2}-- The following {color.CWHITE}{len(partitionsThatAreUnmounted)}' + \
                f'{color.CBLUE2} devices on {color.CWHITE}{ipv4}{color.CBLUE2} are not mounted!{color.CEND}\n')
        for idx, partition in enumerate(partitionsThatAreUnmounted):
            print(f'   {color.CGREEN2}{idx+1:>3}. {color.CEND}Device ' + \
                    f'{color.CCYAN}/dev/{partition["name"]}{color.CEND} has no mount point!')

# ------------------------------------------------------------------------------------------------------

@time_show
@handle_spinner
def mount_dev_partitions(ipv4: str | None = None, spinner: Spinner | None = None):
    if ipv4 and not is_server_active(ipv4 = ipv4):
        raise ConnectionError(f'Error: {ipv4} is not reachable!')

    availablePartitions = get_lsblk_mountable_partitions(ipv4 = ipv4)
    partitionsThatAreUnmounted = [ x for x in availablePartitions if x['mountpoints'] == [ None ] ]
    partitionsThatAreAlreadyMounted = [ x for x in availablePartitions if x['mountpoints'] != [ None ] ]
    print('')
    if not partitionsThatAreUnmounted:
        print(f'{color.CRED2}-- There are no available partitions to mount! ' + \
                f'{color.CWHITE}All device partitions are mounted!{color.CEND}')
        show_dev_partitions(ipv4 = ipv4,
                partitionsThatAreAlreadyMounted = partitionsThatAreAlreadyMounted,
                partitionsThatAreUnmounted = partitionsThatAreUnmounted)
        return

    msg = f'''....  {color.CYELLOW2}{len(partitionsThatAreUnmounted)}{color.CEND} of \
{color.CVIOLET2}{len(availablePartitions)}{color.CEND} partitions are available to be mounted!
'''
    print(msg)

    for idx, partition in enumerate(partitionsThatAreUnmounted):
        mountingPhrase = f'       Mounting {color.CCYAN}/dev/{partition["name"]}{color.CEND} ......   {color.CYELLOW}'
        print(mountingPhrase, end=' ', flush=True)
        spinner.start()
        cmdResult = run_cmd(ipv4, f"udisksctl mount -b /dev/{partition['name']}", timeout=15)
        duration = spinner.stop()
        print('\r', end='', flush=True)
        print(f'{color.CGREEN}-- {color.CWHITE}{idx+1:>3}. ' + \
                f'{color.CGREEN}Mounted {color.CCYAN}/dev/{partition["name"]}' + \
                f'{color.CEND} in {color.CVIOLET2}{duration}{color.CEND}')

    show_dev_partitions(ipv4 = ipv4)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

'''
if __name__ == "__main__":
    try:
        import argcomplete, argparse

        parser = argparse.ArgumentParser(
                    description='Media Manager Paths',
                    epilog='')

        subparsers = parser.add_subparsers(dest='cmd')

        parser_showDriveInfo = subparsers.add_parser('drive.info', help='show drive info on a given server')
        parser_showDriveInfo.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')

        parser_getDrivePaths = subparsers.add_parser('drive.paths', help='show drive paths on a server')
        parser_getDrivePaths.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')
        parser_getDrivePaths.add_argument("--type", default="plex", metavar='<srvType>', choices=['plex', 'worker'], help='Server types')

        parser_getFullSearchPathsAllDrives = subparsers.add_parser('get.search.paths', help='get full search paths from all drives')
        parser_getFullSearchPathsAllDrives.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')
        parser_getFullSearchPathsAllDrives.add_argument("--type", default="plex", metavar='<srvType>', choices=['plex', 'worker'], help='Server types')

        parser_getAllMediaPaths = subparsers.add_parser('get.all.media.paths', help='get all media paths')
        parser_getAllMediaPaths.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')
        parser_getAllMediaPaths.add_argument("--type", default="plex", metavar='<srvType>', choices=['plex', 'worker'], help='Server types')

        parser_getFilteredMediaPaths = subparsers.add_parser('get.filtered.paths', help='get filtered local  media paths')
        parser_getFilteredMediaPaths.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')
        parser_getFilteredMediaPaths.add_argument("--type", default="plex", metavar='<srvType>', choices=['plex', 'worker'], help='Server types')

        parser_getLsblkDevicesAndMounts = subparsers.add_parser('get.lsblk.mounts', help='get lsblk devices and mount paths')
        parser_getLsblkDevicesAndMounts.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')

        parser_showDevicePartitions = subparsers.add_parser('show.dev.partitions', help='display device partitions (mounted and unmounted)')
        parser_showDevicePartitions.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')

        parser_mountDevicePartitions = subparsers.add_parser('mount.dev.partitions', help='mount any mountable device partitions')
        parser_mountDevicePartitions.add_argument("--ipv4", default=None, metavar='<addr>', help='Server IPV4')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.cmd == 'drive.info':
            show_drive_info(ipv4=args.ipv4)

        elif args.cmd == 'drive.paths':
            print("-" * 100)
            print(f"{colors.fg.yellow}Drive Paths ({args.ipv4 if args.ipv4 else 'Local'})!{colors.off}")
            print("-" * 100)
            paths = get_drive_paths(ipv4=args.ipv4, serverType=args.type)
            for idx, path in enumerate(paths):
                print(f"{colors.fg.lightgreen}{idx+1:>3}. {colors.fg.green}{path}{colors.off}")
                if idx % 20 == 19:
                    print("-" * 100)
            print("-" * 100)

        elif args.cmd == 'get.full.search.paths.all.drives':
            print("-" * 100)
            print(f"{colors.fg.yellow}Get Full Search Paths All Drives from {args.ipv4 if args.ipv4 else 'Local'}!{colors.off}")
            print("-" * 100)
            paths = get_full_search_paths_all_drives(ipv4=args.ipv4, serverType=args.type)
            for idx, path in enumerate(paths):
                print(f"{colors.fg.blue}{idx+1:>3}. {colors.fg.cyan}{path}{colors.off}")
                if idx % 20 == 19:
                    print("-" * 100)
            print("-" * 100)

        elif args.cmd == 'get.all.media.paths':
            print("-" * 100)
            print(f"{colors.fg.yellow}Get All Media Paths ({args.ipv4 if args.ipv4 else 'Local'})!{colors.off}")
            print("-" * 100)
            paths = get_all_media_paths(ipv4=args.ipv4, serverType=args.type)
            for idx, path in enumerate(paths):
                print(f"{colors.fg.lightgreen}{idx+1:>3}. {colors.fg.green}{path}{colors.off}")
                if idx % 20 == 19:
                    print("-" * 100)
            print("-" * 100)

        elif args.cmd == 'get.filtered.paths':
            print("-" * 100)
            print(f"{colors.fg.yellow}Get Filtered Media Paths ({args.ipv4 if args.ipv4 else 'Local'})!{colors.off}")
            print("-" * 100)
            paths = get_filtered_media_paths(ipv4=args.ipv4, serverType=args.type)
            for idx, path in enumerate(paths):
                print(f"{colors.fg.blue}{idx+1:>3}. {colors.fg.lightblue}{path}{colors.off}")
                if idx % 20 == 19:
                    print("-" * 100)
            print("-" * 100)

        elif args.cmd == 'get.lsblk.mounts':
            print("-" * 100)
            print(f"{colors.fg.yellow}Get <lsblk> Devices & Mount Paths ({args.ipv4 if args.ipv4 else 'Local'})!{colors.off}")
            print("-" * 100)
            mountablePartitions = get_lsblk_mountable_partitions(ipv4=args.ipv4)
            for idx, partition in enumerate(mountablePartitions):
                print(f"{colors.fg.blue}{idx+1:>3}. {colors.fg.lightblue}{json.dumps(partition, indent=2)}{colors.off}")
                if idx % 20 == 19:
                    print("-" * 100)
            print("-" * 100)

        elif args.cmd == 'show.dev.partitions':
            show_dev_partitions(ipv4=args.ipv4)

        elif args.cmd == 'mount.dev.partitions':
            mount_dev_partitions(ipv4=args.ipv4)

    except Exception as e:
        exception_details(e, "Media Path")
'''
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

