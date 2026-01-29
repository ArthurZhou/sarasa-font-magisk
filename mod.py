import sys
from fontTools.ttLib import TTFont
import os
import zipfile

font = TTFont("Sarasa.ttf", recalcBBoxes = False)
print("reading default sarasa font at ./Sarasa.ttf")

# try to fix the colon error
# if not fixed, android clock may display an empty box in the widget
print("fixing colon")
colon = 0x003A
fancyColon = 0xEE01
for table in font['cmap'].tables:
    if colon in table.cmap:
        table.cmap[fancyColon] = table.cmap[colon]


# align to Roboto
print("align to Roboto")
head_ = font['head']
os2_ = font['OS/2']
upm = head_.unitsPerEm

robotoYMax = 2163
robotoYMin = -555
robotoUpm = 2048
minToMax = (robotoYMax - robotoYMin) / robotoUpm * upm

USE_TYPO_METRICS = 0x80
if os2_.fsSelection & USE_TYPO_METRICS:
	ascender = os2_.sTypoAscender
	descender = os2_.sTypoDescender
else:
	ascender = os2_.usWinAscent
	descender = -os2_.usWinDescent

head_.yMax = round(ascender / (ascender - descender) * minToMax)
head_.yMin = round(descender / (ascender - descender) * minToMax)

# save patched font directly into the module
print("saving to ./magisk/system/fonts/Roboto-Regular.ttf")
font.save("./magisk/system/fonts/Roboto-Regular.ttf")


# pack into zip
print("packing into zip")
with zipfile.ZipFile("Sarasa-font-replacer.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("magisk"):
        for file in files:
            file_path = os.path.join(root, file)
            # this ensures the ZIP root starts inside your magisk folder
            arcname = os.path.relpath(file_path, "magisk")
            zipf.write(file_path, arcname)

print("done! flash Sarasa-font-replacer.zip to magisk now!")

