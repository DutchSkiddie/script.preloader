import os
import xbmc
import xbmcaddon
import xbmcgui

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
    pathpresets = os.path.join(pathaddon, 'resources', 'presets')
    pathcustoms = [os.path.join(pathkodi, 'userdata', 'addon_data', 'script.preloader'), os.path.join(pathaddon, 'resources', 'custom')]
    pathrepos = os.path.join(pathaddon, 'resources', 'presets', 'repos.zip')
    
    return [pathkodi, pathaddons, pathpresets, pathcustoms, pathrepos]

def GetSkin():
    currentskin = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue","id":1,"params":{"setting":"lookandfeel.skin"}}')
    currentskin = currentskin.split('value":"')[1]
    currentskin = currentskin.replace('"}}', '')
    return currentskin

def SetSkin(skinid):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"' + skinid + '"}}')

def SetLang():
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"locale.audiolanguage","value":"English"}}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"locale.subtitlelanguage","value":"English"}}')

def GetPlugins():
    [pathkodi, pathaddons, pathpresets, pathcustoms, pathrepos] = Paths()
    pluginnames = []
    for folder in os.listdir(pathkodi):
        if(folder == 'addons'):
            for pluginfolder in os.listdir(os.path.join(pathkodi, folder)):
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
    
def SetMainPlayer(mainplayer):
    if (mainplayer == 'plugin.video.thecrew'):
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_movies', 'thecrew.json play_movie')
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_episodes', 'thecrew.json play_episode')
        
    if (mainplayer == 'plugin.video.seren'):
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_movies', 'seren.json play_movie')
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_episodes', 'seren.json play_episode')
        
    if (mainplayer == 'plugin.video.fen'):
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_movies', 'fen.json play_movie')
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_episodes', 'fen.json play_episode')
        
    if (mainplayer == 'plugin.video.fenlight'):
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_movies', 'fenlight.json play_movie')
        xbmcaddon.Addon('plugin.video.themoviedb.helper').setSetting('default_player_episodes', 'fenlight.json play_episode')
        
def FixSeren(pathaddons):
    path = os.path.join(pathaddons, 'plugin.video.seren', 'resources', 'lib', 'modules', 'globals.py')
    with open(path, 'r+', encoding="utf8") as file:
        txt = file.read()
        newtxt = txt.replace('''
        elif self.KODI_VERSION == 20:
            return "121"''', '''
        elif self.KODI_VERSION == 20:
            return "121"
        elif self.KODI_VERSION == 21:
            return "131"''')
        file.write(newtxt)
    xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'Seren fix applied, ignore the error.')