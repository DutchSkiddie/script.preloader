import os
import xbmc
import xbmcaddon
import xbmcgui
from resources.lib import lists
from resources.lib import vars
from resources.lib import dialog
from resources.lib import archive
from resources.lib import scrub


def EnableAddon(id):    
    try:
        print(str(xbmcaddon.Addon(id)))
    except:
        xbmc.executebuiltin('EnableAddon("' + id + '")')
        xbmc.sleep(1000)
        while(xbmcgui.getCurrentWindowDialogId() == 10100):
            xbmc.sleep(500)
            
def EnableAddons(addonlist):
    defaultaddons = ['repository.jurialmunkey','repository.otaku','repository.thecrew','skin.arctic.horizon.2','script.trakt','script.embuary.info','plugin.video.themoviedb.helper','plugin.video.thecrew','plugin.video.otaku']
    for addon in addonlist:
        EnableAddon(addon)
        
def ForceUpdate():
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('ReloadSkin(reload)')
    
    
def SetSkin(skinid):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"' + skinid + '"}}')
    

def Setup(setupchoice):
    pathkodi, pathpresets, pathcustoms, pathaddons, lastused, lastusedpreset, lastusedaddons, lastusedaddonconfigtxt, currentplugins = vars.init()
    pathaddons = pathkodi + os.sep + 'addons'
    pathuserdata = pathkodi + os.sep + 'userdata'
    pathaddon = os.path.dirname(os.path.dirname(pathcustoms))
    
    if(setupchoice == 0):
        [zip, zips] = archive.SelectZip(lastused, pathcustoms)
    if(setupchoice == 1):
        [zip, zips] = archive.SelectZip(lastusedpreset, pathpresets)
    if(setupchoice == 2):
        zip = []   
        
    if(setupchoice == 0) or (setupchoice == 1):    
        addons, addonconfig = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi)
        skin = str(addonconfig[0])
        vars.SetCustomSettings(zip, addonconfig, addons)
        dialog.ConfirmSetup()
        notify = dialog.NotificationToggle()
        archive.ExtractZip(notify, pathkodi, zip)
        ForceUpdate()
        EnableAddons(addonconfig)
        SetSkin(skin)
        
    if(setupchoice == 2):
        scrub.ClearApis(pathkodi)
        ForceUpdate()
        addons, addonconfig = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi)
        skin = str(addonconfig[0])
        archive.ArchiveZip(pathaddons, pathuserdata, pathaddon, skin, pathkodi)
            
        
def Exit(setupchoice):
    xbmc.sleep(2000)
    while(xbmcgui.getCurrentWindowDialogId() == 10100):
        xbmc.sleep(500)
    if (setupchoice == 0) or (setupchoice == 1):
        xbmc.sleep(10000)
    xbmcgui.Dialog().ok('Preloader', 'Thanks for using Preloader <3')
    exit()