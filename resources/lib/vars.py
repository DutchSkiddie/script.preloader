import os
import xbmcaddon
import xbmc

addon = xbmcaddon.Addon()
addonpath = os.path.dirname(addon.getAddonInfo('path'))
pathpresets = os.path.join(addonpath, 'resources', 'presets')
pathcustom = os.path.join(addonpath, 'resources', 'custom')
pathaddons = os.path.dirname(addonpath)
pathpackages = os.path.join(pathaddons, 'packages')
pathkodi = os.path.dirname(pathaddons)
pathuserdata = os.path.join(pathkodi, 'userdata')
pathaddondata = os.path.join(pathuserdata, 'addon_data')
pathaddonuserdata = os.path.join(pathaddondata, 'script.preloader')
pathbackups = os.path.join(pathaddonuserdata, 'backups')
pathuserdatacustom = os.path.join(pathaddonuserdata, 'custom')

def Addon():
    return addon

def AddonPath():
    return addonpath

def PathPresets():
    return pathpresets

def PathCustom():
    return pathcustom

def PathAddons():
    return pathaddons

def PathKodi():
    return pathkodi

def PathUserdata():
    return pathuserdata

def PathAddondata():
    return pathaddondata

def PathAddonUserdata():
    return pathaddonuserdata

def PathUserdataCustom():
    return pathuserdatacustom

def PathPackages():
    return pathpackages

def PathBackups():
    return pathbackups

def AddonTypes():
    types = ['skin', 'script', 'movie provider', 'anime provider', 'tracking provider', 'widget', 'resource', Buttons.btn_continue]
    return types

def LocalAddons():
    addons = []
    repos = []
    for root, dirs, files in os.walk(pathaddons):
        for file in files:
            if 'packages' not in root and 'temp' not in root:
                if 'addon.xml' in file:
                    if 'repository' in root:
                        repos.append(str(root).split(os.sep)[-1])
                    else:
                        addons.append(str(root).split(os.sep)[-1])
    return addons, repos

def SetLang():
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"locale.audiolanguage","value":"English"}}')
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"locale.subtitlelanguage","value":"English"}}')
    
def SetSkin(skinid):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"' + skinid + '"}}')
    
def GetSkin():
    currentskin = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue","id":1,"params":{"setting":"lookandfeel.skin"}}')
    currentskin = currentskin.split('value":"')[1]
    currentskin = currentskin.replace('"}}', '')
    return currentskin

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
        
def ah2xbmcversion():
    path = os.path.join(PathAddons(), 'skin.arctic.horizon.2', 'addon.xml')
    with open(path, 'r+', encoding='utf-8') as file:
        txt = file.read()
        newtxt = txt.replace('<import addon="xbmc.gui" version="5.15.0" />', '<import addon="xbmc.gui" version="5.17.0" />')
        file.seek(0)
        file.write(newtxt)
        file.truncate()
    
def serenkodiversion():
    path = os.path.join(PathAddons(), 'plugin.video.seren', 'resources', 'lib', 'modules', 'globals.py')
    with open(path, 'r+', encoding="utf8") as file:
        txt = file.read()
        if 'self.KODI_VERSION == 21:' not in txt:
            newtxt = txt.replace('''
            elif self.KODI_VERSION == 20:
                return "121"''', '''
            elif self.KODI_VERSION == 20:
                return "121"
            elif self.KODI_VERSION == 21:
                return "131"''')
            file.seek(0)
            file.write(newtxt)
            file.truncate()
            
class Buttons:
    btn_continue = '[[COLOR limegreen][B]CONTINUE[/B][/COLOR]]'
    keywords = ['CONTINUE','ADD','NEW']