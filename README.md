# TCX Edit ⌚🏃‍♂️
A simple script for editing the time stamps of TCX files. 

## Motivation
The main usecase for this is if you have a watch where the battery has died. When initially charged, the time will reset to factory settings, typically January 1, 20XX. 

If an activity is recorded before syncing, the time stamps of the activity will be incorrect.

## Installation
Currently, there are no external libraries! 👊

## Usage
```py
python main.py my-file.tcx 2025-07-30T18:15:00
```