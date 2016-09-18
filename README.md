
# BinjaDock 
![screenshot](https://defunctio.github.io/screenshot.png)

BinjaDock allows you to create dockable widgets in Binja and exposes a main dockwidget with tabs for plugins to embed to.

Yarascan is an example plugin demonstrating how to use BinjaDock.

## Installation
Put it in the plugins folder...

## Yarascan 
To use the included yara example plugin you will need to supply your own yara signatures and define them in SIG_FILE in [yarascan.py](https://github.com/NOPDev/BinjaDock/blob/c946abf4202fb070700bef5f49050c879fb95e73/yarascan.py#L38). 
You may find the crypto signatures and many more (AntiVM, malware, packers, exploit kits) [here](https://github.com/Yara-Rules/rules). 

## Requirements
* PyQt5
* yara
* binaryninja...

BinjaDock has only been tested on Ubuntu 16.04 using Qt and PyQt5 packages from the official ubuntu repositories.
