#!/usr/bin/env python3

"""
Black Lantern Security
@Authors
Kerry Milan (Github: kerrymilan)
Micheal Reski (Github: Aconite33, Twitter: @zeekzack)
@Updated to pylnk3
FunnyWhale (Github: FunnyWhaleDev)
Script to generate Windows shortcut (.lnk) files using pylnk3.

Examples:
  # Shortcut directly to a target
  python lnk.py output.lnk C:/Windows/System32/cmd.exe

  # Shortcut to a folder
  python lnk.py folder.lnk C:/Users/Public/ -d

  # Shortcut with arguments for the target
  python lnk.py output.lnk C:/Windows/System32/cmd.exe -a "/c powershell.exe -ep bypass"

  # Shortcut with a specified icon
  python lnk.py output.lnk C:/Windows/System32/cmd.exe -i "c:/windows/system32/notepad.exe"

  # Shortcut with a description
  python lnk.py output.lnk C:/Windows/System32/cmd.exe --desc "This is a description"
"""

import sys
import pylnk3  # Importing pylnk3 instead of pylnk
import argparse
from datetime import datetime

def create_lnk(name, target, mode, args, description, icon, working_dir, is_dir=False):
    # Ensure ".lnk" extension
    if not name.endswith(".lnk"):
        name += ".lnk"

    # Format the target path
    target = target.replace("/", "\\").rstrip("\\").split("\\")
    target_drive, target_file = target[0], target[-1]

    # Format icon path, if provided
    if icon:
        icon = icon.replace("/", "\\").rstrip("\\")

    # Create the .lnk object
    lnk = populate_lnk(name, target, mode, args, description, icon, working_dir)

    # Build target path structure for shell item ID list
    elements = [pylnk3.RootEntry(pylnk3.ROOT_MY_COMPUTER), pylnk3.DriveEntry(target_drive)]
    elements += [build_entry(level) for level in target]
    
    # Mark the target file as a file or directory based on is_dir
    entry = build_entry(target_file)
    entry.type = pylnk3.TYPE_FILE if not is_dir else pylnk3.TYPE_FOLDER
    elements.append(entry)

    lnk.shell_item_id_list = pylnk3.LinkTargetIDList()
    lnk.shell_item_id_list.items = elements

    # Save the .lnk file
    write_lnk(lnk)
    return 0

def populate_lnk(name, target, mode, args, description, icon, working_dir):
    lnk = pylnk3.create(name)
    lnk.specify_local_location("\\".join(target))

    # Set link metadata
    lnk._link_info.size_local_volume_table = 0
    lnk._link_info.volume_label = ""
    lnk._link_info.drive_serial = 0
    lnk._link_info.local = True
    lnk.window_mode = mode

    if args:
        lnk.arguments = args
    if description:
        lnk.description = description
    if icon:
        lnk.icon, lnk.icon_index = icon, 0

    # Set working directory or target path as fallback
    if working_dir:
        working_dir = working_dir.replace("/", "\\").rstrip("\\").split("\\")
        lnk.working_dir = "\\".join(working_dir) + "\\"
    else:
        target.pop()
        lnk.working_dir = "\\".join(target) + "\\"
    
    return lnk

def build_entry(name):
    """Helper to create PathSegmentEntry objects for each directory level."""
    entry = pylnk3.PathSegmentEntry()
    entry.type = pylnk3.TYPE_FOLDER
    entry.file_size = 0
    now = datetime.now()
    entry.modified = entry.created = entry.accessed = now
    entry.short_name = entry.full_name = name
    return entry

def write_lnk(lnk):
    """Writes the shortcut to disk."""
    with open(lnk.file, 'wb') as f:
        lnk.write(f)

def main():
    parser = argparse.ArgumentParser(prog='lnk.py', description='Create a Shortcut (.lnk)')
    parser.add_argument('-d', '--directory', action='store_true', dest='is_dir', 
                        help='Target is a directory')
    parser.add_argument('name', help='Name of shortcut file')
    parser.add_argument('target', help='Target file path')
    parser.add_argument('-a', '--arguments', help='Arguments to add to the target')
    parser.add_argument('--mode', choices=['Maximized', 'Normal', 'Minimized'], 
                        default='Minimized', help='Window mode for the shortcut (default: Minimized)')
    parser.add_argument('--desc', dest='description', help='Description for the shortcut')
    parser.add_argument('-i', '--icon', help='Icon for the shortcut')
    parser.add_argument('-w', '--working', dest='working_dir', help='Specify working directory')
    
    args = parser.parse_args()
    return create_lnk(args.name, args.target, args.mode, args.arguments, args.description, args.icon, args.working_dir, args.is_dir)

if __name__ == "__main__":
    sys.exit(main())
