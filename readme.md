# lnk.py
___
Repository used for creating lnk file for Windows. Can be used on Linux systems or Windows systems for the creation of the Windows lnk file.

Requires Python 2 (pylnk does not support python 3)

Examples:

Shortcut direct to a target
```
python lnk.py output.lnk C:/Windows/System32/cmd.exe
```

Shortcut to a folder
```
python lnk.py folder.lnk C:/Users/Public/ -d
```

Shortcut direct to a target with arguments
```
python lnk.py output.lnk C:/Windows/System32/cmd.exe -a "/c powershell.exe -ep bypass"
```

Shortcut direct to a target specifying icon
```
python lnk.py output.lnk C:/Windows/System32/cmd.exe -i "c:/windows/system32/notepad.exe"
```

Shortcut direct to a target with a description
```
python lnk.py output.lnk C:/Windows/System32/cmd.exe --desc "This is a description"
```

# Authors
### [Black Lantern Security](https://www.blacklanternsecurity.com)
[Kerry Milan](https://github.com/kerrymilan)

[Micheal Reski](https://github.com/aconite33) [@zeekzack](https://twitter.com/@zeekzack)