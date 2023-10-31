# DL2IDScript

***
A simple Python3 script for quickly creating and up-to-date Infinite Weapon Durability mod for Dying Light 2

## How to use

***

### Using Python (Recommended)

1. Install [Python 3](https://www.python.org/) for your system.
2. Download `DL2IDScript.py`.
    1. To download, click on `DL2IDScript.py` and click on `Download raw file`.
3. Place `DL2IDScript.py` into the same folder as your `data0.pak` file.
    1. On Steam, right-click `Dying Light 2`, go under *Manage*, then click on *Browse local files*.
    2. Open the `ph` folder and then the  `source` folder. `data0.pak` should be in there.
4. Open up Command Prompt (or your terminal of choice) in the source folder.
    1. On Windows 11, you can right-click an empty spot and select *Open in Terminal*.
    2. On Windows 10 and lower, you can hold `Shift` while right-clicking an empty spot and select *Open command window
       here*.
5. Type the following in the terminal and hit `Enter`

```commandline
python DL2IDScript.py
```

6. Follow the prompts to generate an up-to-date mod.

### Using the executable

1. Download the newest `DL2IDScript.zip` from the [*Releases*](https://github.com/Lomeli12/DL2IDScript/releases) page.
2. Open the zip file and copy `DL2IDScript.exe` and `msys-2.0.dll` into the same folder as your `data0.pak` file.
    1. On Steam, right-click `Dying Light 2`, go under *Manage*, then click on *Browse local files*.
    2. Open the `ph` folder and then the  `source` folder. `data0.pak` should be in there.
3. Double-click on `DL2IDScript.exe` and follow the prompts to generate an up-to-date mod.

## Known issues

* During events, the event break the player variable files this script patches for infinite weapon durability. Playing
  in offline mode until the event ends might solve this issue. See 
  [here](https://forums.nexusmods.com/index.php?/topic/11042943-unlimited-weapon-durability/page-16#entry114300993). 

## Thanks to

* [Nuitka](https://github.com/Nuitka/Nuitka), used to create executable file.
* Obscene911 from the NexusMods forum, for explaining 
  [how to create your own infinite weapon durability mod.](https://forums.nexusmods.com/index.php?/topic/11042943-unlimited-weapon-durability/page-15#entry113433628)