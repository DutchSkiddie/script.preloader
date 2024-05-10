import os
import xbmc
import xbmcaddon
import xbmcgui
from resources.lib import lists
from resources.lib import vars
from resources.lib import dialog
from resources.lib import archive

def InstallAddons(addons, pathaddons):
    for addon in addons:
        xml = os.path.join(pathaddons, addon, 'addon.xml')
        
        if (addon.startswith('repo')):
            InstallAddon(addon, xml)
    
    for addon in addons:
        xml = os.path.join(pathaddons, addon, 'addon.xml')    
        InstallAddon(addon, xml)
        if (addon == 'plugin.video.seren'):
            vars.FixSeren(pathaddons)
        

def DialogCheck():    
    def DialogPass():
        xbmc.sleep(75)
        if (xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
            while(xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
                xbmc.sleep(500)
            return True
        else:
            return False
    
    p1 = True
    p2 = True
    p3 = True
    p4 = True
    while(p1 or p2 or p3 or p4):
        p1 = DialogPass()
        p2 =DialogPass()
        p3 =DialogPass()
        p4 = DialogPass()

def InstallAddon(addon, xml):
    version = 0
    while (version == 0):
        try:
            DialogCheck()
            if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                xbmc.executebuiltin('InstallAddon("' + addon + '")')
            DialogCheck()
            if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                if XMLExists(xml):
                    version = xbmcaddon.Addon(addon).getAddonInfo('version')
        except:
            DialogCheck()
            if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                xbmc.executebuiltin('EnableAddon("' + addon + '")')

def XMLExists(pathaddon):
    return os.path.exists(pathaddon)

        
def ForceUpdate():
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('ReloadSkin(reload)')
    

def Setup(setupchoice):
    pathkodi, pathpresets, pathcustoms, pathrepos, pathaddons, lastused, lastusedpreset, lastusedaddons, lastusedaddonconfigtxt = vars.init()
    pathaddons = os.path.join(pathkodi, 'addons')
    pathuserdata = os.path.join(pathkodi, 'userdata')
    
    if(setupchoice == 0):
        [zip, config] = archive.SelectZip(lastused, pathcustoms)
    if(setupchoice == 1):
        zip = []
    if(setupchoice == 2):
        zip = []
        zipuserdata = [] 
        
    if(setupchoice == 0):
        if (config == False):
            addons, addonconfig, presetchoice, repos, mainvideoplayer = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi, pathpresets) 
        else:
            addons = config
            addonconfig = config
            presetchoice = False
            mainvideoplayer = ''
        skin = str(addonconfig[0])
        vars.SetCustomSettings(zip, addonconfig, addons)
        dialog.ConfirmSetup()
        notify = dialog.NotificationToggle()
        archive.ExtractZip(notify, pathkodi, zip, presetchoice)
        ForceUpdate()
        InstallAddons(addonconfig, pathaddons)
        vars.SetLang()
        vars.SetMainPlayer(mainvideoplayer)
        thanks()
        vars.SetSkin(skin)
        
    if(setupchoice == 1):    
        addons, addonconfig, presetchoice, repos, mainvideoplayer = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi, pathpresets)
        skin = str(addonconfig[0])
        zipuserdata = os.path.join(pathpresets, skin + '.zip')
        zipoptionals = os.path.join(pathpresets, 'optionals.zip')
        vars.SetCustomSettings(zip, addonconfig, addons)
        dialog.ConfirmSetup()
        notify = dialog.NotificationToggle()
        archive.ExtractZip(notify, pathkodi, pathrepos, repos)
        ForceUpdate()
        InstallAddons(addonconfig, pathaddons)
        archive.ExtractZip(notify, pathkodi, zipuserdata, presetchoice)
        archive.ExtractZip(notify, pathkodi, zipoptionals, addonconfig)
        vars.SetLang()
        vars.SetMainPlayer(mainvideoplayer)
        thanks()
        vars.SetSkin(skin)
    if(setupchoice == 2):
        skin = vars.GetSkin()
        savetype = dialog.ChooseSaveType()
        if (savetype == False):
            setupchoice = 3
        addons, addonconfig, presetchoice, repos, mainvideoplayer = lists.AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi, pathpresets)
        notify = dialog.NotificationToggle()
        archive.ArchiveZip(pathaddons, pathuserdata, skin, pathkodi, savetype, addonconfig, repos)
        thanks()
 
        
def thanks():
    xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'Thanks for using preloader <3.')