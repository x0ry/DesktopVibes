# DesktopVibes
Powershell + Python script to cycle your desktop wallpaper in windows 10 and color sync with your Phillips Hue lights.

This is a working MVP, feel free to contribute cleaner better usable code.

pip install phue - https://github.com/studioimaginaire/phue

powershell ./test.ps1
//will change the desktop wallpaper based on a folder of images.

python ./test.py
//will read windows 10's color selection and auto set as your highlight/tracking color - also converts RGB to XY for casting to your phillips hue bridge.
