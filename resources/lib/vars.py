import os
import xbmc
import xbmcaddon

def init():
    [pathkodi, pathaddons, pathpresets, pathcustoms] = Paths()
    lastused = xbmcaddon.Addon().getSetting('lastused')
    lastusedpreset = xbmcaddon.Addon().getSetting('lastusedpreset')
    lastusedaddons = xbmcaddon.Addon().getSetting('lastusedaddons')
    lastusedaddonconfigtxt = xbmcaddon.Addon().getSetting('lastusedaddonconfig')
    currentplugins = GetPlugins(pathkodi)
    
    return pathkodi, pathpresets, pathcustoms, pathaddons, lastused, lastusedpreset, lastusedaddons, lastusedaddonconfigtxt, currentplugins

def Paths():
    addon = xbmcaddon.Addon()
    addonpath = addon.getAddonInfo('path')
    pathaddon = os.path.dirname(addonpath)
    pathaddons = os.path.dirname(pathaddon)
    pathkodi = os.path.dirname(pathaddons)
    pathpresets = pathaddon + os.sep +'resources' + os.sep + 'presets' + os.sep
    pathcustoms = pathaddon + os.sep + 'resources' + os.sep + 'custom' + os.sep
    
    return [pathkodi, pathaddons, pathpresets, pathcustoms]

def GetSkin():
    currentskin = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue","id":1,"params":{"setting":"lookandfeel.skin"}}')
    currentskin = currentskin.split('value":"')[1]
    currentskin = currentskin.replace('"}}', '')
    return currentskin

def GetPlugins(path):
    pluginnames = []
    for folder in os.listdir(path):
        if(folder == 'addons'):
            for pluginfolder in os.listdir(path + os.sep + folder):
                strpluginfolder = str(pluginfolder)
                if (strpluginfolder.startswith('metadata') == False) and (strpluginfolder != 'packages') and (strpluginfolder != 'temp') and (strpluginfolder.startswith('script.common') == False) and (strpluginfolder.startswith('script.module') == False) and (strpluginfolder.startswith('service.xbmc') == False):
                    pluginnames.append(strpluginfolder)
    return pluginnames 

def SetCustomSettings(ziploc, lastusedaddonconfig, lastusedaddons):
    xbmcaddon.Addon().setSetting('lastused', str(ziploc))    
    xbmcaddon.Addon().setSetting('lastusedaddonconfig', str(lastusedaddonconfig))
    xbmcaddon.Addon().setSetting('lastusedaddons', str(lastusedaddons))