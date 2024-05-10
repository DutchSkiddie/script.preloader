import xbmcgui
from resources.lib import archive

def Welcome():
    response = xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'Make sure to back up your settings!')
    if(response == False):
        exit()
    setupchoice = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]Preloader[/COLOR]', 'What do you want to do?','Save my Files', 'Custom', 'Preset')
    return setupchoice        

def ConfirmSetup():
    confirm = xbmcgui.Dialog().yesno('[COLOR orange][B]WARNING[/B][/COLOR]', 'You are about to overwrite your userdata folder.\n Are you sure?')
    if(confirm == False):
        exit()
        
def ChooseSaveType():
    choice = xbmcgui.Dialog().yesno('[COLOR firebrick]Preloader[/COLOR]', 'Save as', 'CONFIG', 'BACKUP')
    return choice
        
def NotificationToggle():
    notify = xbmcgui.Dialog().yesno('[COLOR orchid][B]SETUP INFO[/B][/COLOR]', 'Do you want details?')
    return notify

def DefaultPlayer():
    choice = xbmcgui.Dialog().yesno('[COLOR firebrick][B]DEFAULT PLAYER[/B][/COLOR]', 'Do you want a default player?')
    return choice

def ChoosePreset(pathskin):    
    choices = archive.FindPresets(pathskin)
    picker = xbmcgui.Dialog().select('Decide your preset (Custom)', choices, 0, 1, False)
    choice = choices[picker]
    
    return choice