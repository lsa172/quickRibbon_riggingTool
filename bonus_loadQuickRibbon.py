'''
Bonus content: this code directly loads the quickRibbon tool from Maya's default script folder, in cas you'd like to 
rework my script while testing it in Maya
Download or transfer quickRibbon.py to Maya's user script folder (usually \Documents\maya\scripts) and run this script
'''
import sys
import imp

import quickRibbon as qrb
imp.reload(qrb)
qrb.quickRibbon()

