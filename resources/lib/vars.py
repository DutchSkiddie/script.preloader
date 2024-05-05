import os
import xbmc
import xbmcaddon

def init():
    [pathkodi, pathaddons, pathpresets, pathcustoms, pathrepos] = Paths()
    lastused = xbmcaddon.Addon().getSetting('lastused')
    lastusedpreset = xbmcaddon.Addon().getSetting('lastusedpreset')
    lastusedaddons = xbmcaddon.Addon().getSetting('lastusedaddons')
    lastusedaddonconfigtxt = xbmcaddon.Addon().getSetting('lastusedaddonconfig')
    
    return pathkodi, pathpresets, pathcustoms, pathrepos, pathaddons, lastused, lastusedpreset, lastusedaddons, lastusedaddonconfigtxt

def Paths():
    addon = xbmcaddon.Addon()
    addonpath = addon.getAddonInfo('path')
    pathaddon = os.path.dirname(addonpath)
    pathaddons = os.path.dirname(pathaddon)
    pathkodi = os.path.dirname(pathaddons)
    pathpresets = pathaddon + os.sep +'resources' + os.sep + 'presets' + os.sep
    pathcustoms = os.path.join(pathkodi, 'userdata', 'addon_data', 'script.preloader')
    pathrepos = os.path.join(pathaddon, 'resources', 'presets', 'repos.zip')
    
    return [pathkodi, pathaddons, pathpresets, pathcustoms, pathrepos]

def GetSkin():
    currentskin = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue","id":1,"params":{"setting":"lookandfeel.skin"}}')
    currentskin = currentskin.split('value":"')[1]
    currentskin = currentskin.replace('"}}', '')
    return currentskin

def GetPlugins():
    [pathkodi, pathaddons, pathpresets, pathcustoms, pathrepos] = Paths()
    pluginnames = []
    for folder in os.listdir(pathkodi):
        if(folder == 'addons'):
            for pluginfolder in os.listdir(pathkodi + os.sep + folder):
                strpluginfolder = str(pluginfolder)
                if (strpluginfolder.startswith('metadata') == False) and (strpluginfolder != 'packages') and (strpluginfolder != 'temp') and (strpluginfolder.startswith('script.common') == False) and (strpluginfolder.startswith('script.module') == False) and (strpluginfolder.startswith('service.xbmc') == False):
                    pluginnames.append(strpluginfolder)
    return pluginnames

def GetRepos():
    repos = []
    plugins = GetPlugins()
    for plugin in plugins:
        if 'repository' in plugin:
            repos.append(plugin)
    return repos

    

def SetCustomSettings(ziploc, lastusedaddonconfig, lastusedaddons):
    xbmcaddon.Addon().setSetting('lastused', str(ziploc))    
    xbmcaddon.Addon().setSetting('lastusedaddonconfig', str(lastusedaddonconfig))
    xbmcaddon.Addon().setSetting('lastusedaddons', str(lastusedaddons))