import os
import xbmc
import xbmcaddon
import xbmcgui
from resources.lib import lists
from resources.lib import vars
from resources.lib import dialog
from resources.lib import archive

def InstallAddons(addons):
    for addon in addons:
        if (addon.startswith('repo')):
            try:
                print(str(xbmcaddon.Addon(addon)))
            except:
                if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                    xbmc.executebuiltin('InstallAddon("' + addon + '")')
                xbmc.sleep(1000)
                while(xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
                    xbmc.sleep(500)
    
    for addon in addons:
        if (addon.startswith('repo')):
            try:
                print(str(xbmcaddon.Addon(addon)))
            except:
                if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                    xbmc.executebuiltin('EnableAddon("' + addon + '")')
                xbmc.sleep(1000)
                while(xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
                    xbmc.sleep(500)
    
    for addon in addons:    
        try:
            print(str(xbmcaddon.Addon(addon)))
        except:
            if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                xbmc.executebuiltin('InstallAddon("' + addon + '")')
            xbmc.sleep(1000)
            while(xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
                xbmc.sleep(500)
                
    for addon in addons:
        try:
            print(str(xbmcaddon.Addon(addon)))
        except:
            if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                xbmc.executebuiltin('EnableAddon("' + addon + '")')
            xbmc.sleep(1000)
            while(xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
                xbmc.sleep(500)

        
def ForceUpdate():
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('ReloadSkin(reload)')
    
    
def SetSkin(skinid):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"' + skinid + '"}}')
    

def Setup(setupchoice):
    pathkodi, pathpresets, pathcustoms, pathrepos, pathaddons, lastused, lastusedpreset, lastusedaddons, lastusedaddonconfigtxt = vars.init()
    pathaddons = pathkodi + os.sep + 'addons'
    pathuserdata = pathkodi + os.sep + 'userdata'
    
    if(setupchoice == 0):
        [zip, config] = archive.SelectZip(lastused, pathcustoms)
    if(setupchoice == 1):
        zip = []
    if(setupchoice == 2):
        zip = []
        zipuserdata = [] 
        
    if(setupchoice == 0):
        if (config == False):
            addons, addonconfig, presetchoice, repos = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi, pathpresets) 
        else:
            addons = config
            addonconfig = config
            presetchoice = False
        skin = str(addonconfig[0])
        vars.SetCustomSettings(zip, addonconfig, addons)
        dialog.ConfirmSetup()
        notify = dialog.NotificationToggle()
        archive.ExtractZip(notify, pathkodi, zip, presetchoice)
        ForceUpdate()
        xbmcgui.Dialog().textviewer('addonconfig', str(addonconfig))
        InstallAddons(addonconfig)
        SetSkin(skin)
        
    if(setupchoice == 1):    
        addons, addonconfig, presetchoice, repos = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi, pathpresets)
        skin = str(addonconfig[0])
        zipuserdata = os.path.join(pathpresets, skin + '.zip')
        vars.SetCustomSettings(zip, addonconfig, addons)
        dialog.ConfirmSetup()
        notify = dialog.NotificationToggle()
        archive.ExtractZip(notify, pathaddons, pathrepos, False)
        archive.ExtractZip(notify, pathkodi, zipuserdata, presetchoice)
        ForceUpdate()
        InstallAddons(addonconfig)
        SetSkin(skin)
        
    if(setupchoice == 2):
        skin = vars.GetSkin()
        savetype = dialog.ChooseSaveType()
        if (savetype == False):
            setupchoice = 3
        addons, addonconfig, presetchoice, repos = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi, pathpresets)
        notify = dialog.NotificationToggle()
        archive.ArchiveZip(pathaddons, pathuserdata, skin, pathkodi, savetype, addonconfig, repos)
            
            
        
def Exit(setupchoice):
    xbmc.sleep(2000)
    while(xbmcgui.getCurrentWindowDialogId() == 10100):
        xbmc.sleep(500)
    if (setupchoice == 0) or (setupchoice == 1):
        xbmc.sleep(10000)
    xbmcgui.Dialog().ok('Preloader', 'Thanks for using Preloader <3')
    exit()