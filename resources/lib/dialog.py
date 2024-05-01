import xbmcgui

def Welcome():
    response = xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'Make sure to back up your settings!')
    if(response == False):
        exit()        

def SetupType():
    setupchoice = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]Preloader[/COLOR]', 'What do you want to do?','Save my Files', 'Custom', 'Preset')
    return setupchoice

def ConfirmSetup():
    confirm = xbmcgui.Dialog().yesno('[COLOR orange][B]WARNING[/B][/COLOR]', 'You are about to overwrite your userdata folder.\n Are you sure?')
    if(confirm == False):
        exit()
        
def NotificationToggle():
    notify = xbmcgui.Dialog().yesno('[COLOR orchid][B]SETUP INFO[/B][/COLOR]', 'Do you want details?')
    return notify