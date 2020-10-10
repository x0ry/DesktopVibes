#!/usr/bin/python
import winreg as _winreg
from phue import Bridge
from rgbxy import Converter
from rgbxy import GamutA # or GamutB, GamutC
import math
# This is based on original code from http://stackoverflow.com/a/22649803

def EnhanceColor(normalized):
    if normalized > 0.04045:
        return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92

def RGBtoXY(r, g, b):
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0

    rFinal = EnhanceColor(rNorm)
    gFinal = EnhanceColor(gNorm)
    bFinal = EnhanceColor(bNorm)
    
    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

    if X + Y + Z == 0:
        return (0,0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)
    
        return (xFinal, yFinal)
converter = Converter(GamutA)
def convertColor(hexCode):
    R = int(hexCode[:2],16)
    G = int(hexCode[2:4],16)
    B = int(hexCode[4:6],16)
    total = R + G + B
    if R == 0:
        firstPos = 0
    else:
        firstPos = R / total
    if G == 0:
        secondPos = 0
    else:
        secondPos = G / total
    return [firstPos, secondPos]
b = Bridge('10.0.0.159')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

root_key=_winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Accent", 0, _winreg.KEY_READ)
[Pathname,regtype]=(_winreg.QueryValueEx(root_key,"AccentPalette"))
_winreg.CloseKey(root_key)
last_chars = (Pathname)#.replace("\\x","").replace("b'","").replace("'","")
finalcolor = ""
for x in last_chars[20:-9]:
    #print(str(x).zfill(2))
    finalcolor = finalcolor + str(((str(hex(x))+" ")[2:4])).zfill(2)
#print(finalcolor)
for l in b.lights:
    if((l.name == "Hue go 1") or (l.name == "Hue lightstrip plus 1") or (l.name == "Hue color lamp 1")):
        #print(l.name)
        #print
        b.get_light(l.name, 'on')
        b.set_light(l.name, 'bri', 254)
        rgbvals = tuple(int(finalcolor[i:i+2], 16) for i in (0, 2, 4))
        print(rgbvals[0],rgbvals[1],rgbvals[2],finalcolor)
        #b.set_light(l.name, 'xy', converter.hex_to_xy(finalcolor))
        b.set_light(l.name, 'xy', RGBtoXY(rgbvals[0],rgbvals[1],rgbvals[2]))
#        print (rgbvals[0])
#        print (rgbvals[1])
#        print (rgbvals[2])
        
        #b.set_light(l.name, 'xy', p(finalcolor))
        
        #b.xy = [random(), random()]
# Prints if light 1 is on or not
#b.get_light(1, 'on')

# Set brightness of lamp 1 to max
#b.set_light(1, 'bri', 254)

# Set brightness of lamp 2 to 50%
#b.set_light(2, 'bri', 127)

# Turn lamp 2 on
#b.set_light(2,'on', True)

# You can also control multiple lamps by sending a list as lamp_id
#b.set_light( [1,2], 'on', True)

# Get the name of a lamp
#b.get_light(1, 'name')

# You can also use light names instead of the id
#b.get_light('Kitchen')
#b.set_light('Kitchen', 'bri', 254)

# Also works with lists
#b.set_light(['Bathroom', 'Garage'], 'on', False)

# The set_light method can also take a dictionary as the second argument to do more fancy stuff
# This will turn light 1 on with a transition time of 30 seconds
#command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}
#b.set_light(1, command)