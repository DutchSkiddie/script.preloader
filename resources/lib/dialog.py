import os
import xbmcgui
from resources.lib import vars
from resources.lib import setup

def SetupType():
    response = xbmcgui.Dialog().yesnocustom("[COLOR firebrick]PRELOADER[/COLOR]\t{[COLOR limegreen]PRELOADED[/COLOR]}", '', 'BACKUP', 'CUSTOM', 'PRESET')
    if response == -1:
        exit()
    elif response == 0:
        return 'custom'
    elif response == 1:
        return 'preset'
    elif response == 2:
        return 'backup'
        
def AskCustomize():
    asking = True
    while asking == True:
        response = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]CUSTOM[/COLOR]', '', 'QUICK-SETUP', 'BACK', 'CONFIGURE')
        if response == -1 or response == 0:
            asking = False
            return -1
        elif response == 1:
            response = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]XML SELECT[/COLOR]', '', '[COLOR goldenrod]~[/COLOR]REPOS[COLOR goldenrod]~[/COLOR]', 'BACK', '[COLOR goldenrod]~[/COLOR]ADDONS[COLOR goldenrod]~[/COLOR]')
            if response == -1 or response == 0:
                continue
            elif response == 1:
                asking = False
                return 'addons'
            elif response == 2:
                asking = False
                return 'repos'
        elif response == 2:
            asking = False
            return 'quicksetup'
        
def ChoosePreset():
    presets = []
    path = vars.PathPresets()
    files = os.listdir(path)
    for file in files:
        if 'skin' in file:
            presets.append(file.replace('.zip', '').replace('skin.', '').replace('.', ' ').title())
    response = xbmcgui.Dialog().select('[COLOR firebrick]|Preloaded|[/COLOR]\t[COLOR goldenrod][SKIN SELECT][/COLOR]', presets, 0, 0, True)
    if response == -1:
        setup.init()
    preset = 'skin.' + str(presets[response]).lower().replace(' ', '.') + '.zip'
    return preset

def ChooseProfile(preset):
    path = vars.PathPresets()
    zip = os.path.join(path, preset)
    profiles = []
    if os.path.exists(zip):
        from zipfile import ZipFile
        with ZipFile(zip, mode='r') as checkup:
            for profile in checkup.namelist():
                if 'addons.xml' in profile:
                    addons = checkup.read(profile)
                elif 'repos.xml' in profile:
                    repos = checkup.read(profile)
                else:
                    profilename = os.path.normpath(profile)
                    profilename = profilename.split(os.sep)[0]
                    if profilename not in profiles:
                        profiles.append(profilename)
    response = xbmcgui.Dialog().select('[COLOR firebrick]|Preloaded|[/COLOR]\t[COLOR goldenrod][PROFILE SELECT][/COLOR]', profiles, 0, 0, True)
    if response == -1:
        setup.init()
    return profiles[response], addons, repos

def Optionals():
    path = vars.PathPresets()
    zip = os.path.join(path, 'optionals.zip')
    if os.path.exists(zip):
        from zipfile import ZipFile
        with ZipFile(zip, mode='r') as checkup:
            for profile in checkup.namelist():
                if 'addons.xml' in profile:
                    addons = checkup.read(profile)
                elif 'repos.xml' in profile:
                    repos = checkup.read(profile)
    return addons, repos

def ChooseOptionals(addons, dependencies):
    path = vars.PathPresets()
    zip = os.path.join(path, 'optionals.zip')
    addondata = os.path.join('userdata', 'addon_data')
    localaddons, localrepos = vars.LocalAddons()
    optionals = []
    if os.path.exists(zip):
        from zipfile import ZipFile
        with ZipFile(zip, mode='r') as checkup:
            for item in checkup.namelist():
                if str(addondata) in os.path.normpath(item):
                    option = os.path.normpath(item)
                    option = option.split(os.sep)[2]
                    if option not in optionals:
                        if option in addons or option in dependencies or option in localaddons:
                            if option not in optionals:
                                optionals.append(option)
    questions = []
    for optional in optionals:
        if 'plugin.video.' in str(optional):
            questions.append('[COLOR firebrick]OVERWRITE[/COLOR] ' + str(optional).title().replace('Plugin.Video.', '[COLOR goldenrod][video plugin][/COLOR] '))
        elif 'script.' in str(optional):
            questions.append('[COLOR firebrick]OVERWRITE[/COLOR] ' + str(optional).title().replace('Script.', '[COLOR goldenrod][script][/COLOR] '))
        elif 'skin.' in str(optional):
            questions.append('[COLOR firebrick]OVERWRITE[/COLOR] ' + str(optional).title().replace('Skin.', '[COLOR goldenrod][skin][/COLOR] '))
    currentoptionals = list(range(0, len(optionals), 1))
    responses = xbmcgui.Dialog().multiselect('[COLOR firebrick]OPTIONS[/COLOR]', questions, 0, currentoptionals)
    answers = []
    if responses != None:
        for response in responses:
            answers.append(questions[response])
        options = []
        for answer in answers:
            if '[video plugin]' in str(answer):
                options.append(str(answer).replace('[COLOR goldenrod][video plugin][/COLOR] ', 'plugin.video.').replace('[COLOR firebrick]OVERWRITE[/COLOR] ', '').lower())
            if '[script]' in str(answer):
                options.append(str(answer).replace('[COLOR goldenrod][script][/COLOR] ', 'script.').replace('[COLOR firebrick]OVERWRITE[/COLOR] ', '').lower())
            if '[skin]' in str(answer):
                options.append(str(answer).replace('[COLOR goldenrod][skin][/COLOR] ', 'skin.').replace('[COLOR firebrick]OVERWRITE[/COLOR] ', '').lower())
        return options
    else:
        setup.init()
        
def Backup():
    asking = True
    while asking == True:
        response = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]BACKUP[/COLOR]', '', 'LOAD', 'BACK', 'SAVE')
        if response == -1 or response == 0:
            exit()
        elif response == 1:
            response = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]SAVE BACKUP[/COLOR]', '', '[COLOR goldenrod]~[/COLOR]CONFIG[COLOR goldenrod]~[/COLOR]', 'BACK', '[COLOR goldenrod]~[/COLOR]FULL BACKUP[COLOR goldenrod]~[/COLOR]')
            if response == -1 or response == 0:
                continue
            elif response == 1:
                asking = False
                return 'savefiles'
            elif response == 2:
                asking = False
                return 'saveconfig'
        elif response == 2:
            pathbackups = os.path.normpath(vars.PathBackups())
            backups = [str(os.path.relpath(os.path.join(root, file), pathbackups)).split(os.sep)[0] for root, dirs, files in os.walk(pathbackups) for file in files if '_full_' in file or '_config_' in file]
            response = xbmcgui.Dialog().select('[COLOR firebrick]|Preloaded|[/COLOR]\t[COLOR goldenrod][BACKUP MANAGER][/COLOR]', backups, 0, 0, True)
            if response == -1:
                continue
            else:
                backup = backups[response]
                asking = False
                return backup