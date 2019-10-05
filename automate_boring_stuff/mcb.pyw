#! C:/Users/neron/Anaconda3/envs/python37 python

###
# Nikola Dordic
# https://nidjo.com
# 21-Avg-2019
###

"""
    mcb.pyw - Saves and loads pieces of text to the clipboard.
    usage: py.exe mcb.pyw save <keyword> - Saves clipboard to keyword.
            py.exe mcb.pyw <keyword> - Loads keyword to clipboard.
            py.exe mcb.pyw list - Loads all keywords to clipboard.


    Project: Multiclipboard
    https://automatetheboringstuff.com/chapter8
"""

import shelve
import pyperclip
import sys

mcbShelve = shelve.open('mcb')

# Save clipboard content
if len(sys.argv == 3) and sys.argv[1].lower() == 'save':
    mcbShelve[sys.argv[2]] = pyperclip.paste()
elif len(sys.argv == 2):
    # List keywords and load content
    if sys.argv[1].lower() == 'list':
        pyperclip.copy(str(list(mcbShelve.keys())))
    elif sys.argv[1] in mcbShelve:
        pyperclip.copy(mcbShelve[sys.argv[1]])


mcbShelve.close()