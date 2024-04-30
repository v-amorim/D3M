# D3M

A Diablo III Macro Collection.
The Macros work on all Resolutions.

## Macros

All Macros are sent directly to Diablo III without using your physical mouse or keyboard.\
This has numerous advantages, such as

- Faster Macro execution time
- Reliability
- Working without Diablo III being in the foreground

## Setting Hotkeys

To set a Hotkey

1. Click the Button next to the Label of the Hotkey you would like to set
2. Press the combination of keys you would like to use
3. Accept the new Combination

You may cancel setting a Hotkey by pressing **Escape**.\
You may delete a Hotkey by clicking and pressing **Delete**.

## Macro Explanations

#### Normalize Difficulty

Sets the Game Difficulty to normal.\
[Video](https://www.youtube.com/watch?v=zOXCv5Dp7b0)

#### Pause D3M

Stops any Hotkey or Screen Listeners.\
[Video](https://www.youtube.com/watch?v=Rp9x4hEfUi8)

#### Port to Ax Town

Ports to the Town of Act x.

#### Open Grift

Opens a Greater Rift from when you have clicked the Obelisk.\
[Video](https://www.youtube.com/watch?v=-PjyOAo1a0I)

#### Upgrade Gem

Upgrades the Gem in the top left Spot.\
[Video](https://www.youtube.com/watch?v=b7HS-NXbUus)\
Set the amount of Upgrades to do before porting to town with the Empowered option.

#### Leave Game

Leaves the Game.\
[Video](https://www.youtube.com/watch?v=1SfbbTvYITY)

#### Salvage / Drop Inventory

Salvages or Drops the Items from your Inventory.\
[Video](https://www.youtube.com/watch?v=q5NzPwmcIP4)\
Spares x Columns looking from the left of the Inventory.
![](https://i.ibb.co/BfdL0kC/spare-columns.png)\
Spare Columns = 0: Salvages the entire Inventory - including the Blue Column\
Spare Columns = 1: Salvages everything besides the Blue Column\
and so on

#### Gamble

Gambles the Itemtype specified in Settings.\
[Video](https://www.youtube.com/watch?v=NJsJpJb3Fas)

#### Convert 1/2-Slot

Converts all the Items in your Inventory whilst taking vertical steps the size of 1/2 Inventory slots.\
E.g. use 1-Slot for Rings and 2-Slot for Gloves.\
The SoL Option does two converting rotations in less time than a non SoL convert takes for one Rotation.

#### Reforge / Convert Set

Reforges or Converts the Item in the top left corner.\
[Video](https://www.youtube.com/watch?v=B3Z23ZkxH4M)

## Compile

```shell
pyinstaller --noconfirm --onefile --console --icon "Style/D3M.ico" --add-data "Style;Style/" --add-data "Style/frameless.qss;."  "gui.pyw"
```
