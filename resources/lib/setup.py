import os
import xbmc
import xbmcgui
import xbmcaddon
import asyncio
from urllib import request
from urllib.error import HTTPError
from resources.lib import dialog
from resources.lib import vars
from resources.lib import lists
from resources.lib import setup
from resources.lib import backup

def init():
    setup = dialog.SetupType()
    
    if setup == 'custom':
        CustomSetup()
    if setup == 'preset':
        PresetSetup()
    if setup == 'backup':
        backup.init()

def InstallAddons(addons):
    pathaddons = vars.PathAddons()
    for addon in addons:                    
        if isinstance(addon, (list, tuple)) and addon != []:
            for dependency in addon:
                if dependency is not None and dependency != []:
                    xml = os.path.join(pathaddons, str(dependency), 'addon.xml')
                    InstallAddon(str(dependency), xml)
        elif addon is not None and addon != []:
            xml = os.path.join(pathaddons, str(addon), 'addon.xml')
            InstallAddon(str(addon), xml)
            
        if (addon == 'plugin.video.seren'):
            vars.serenkodiversion()
        

def DialogCheck():    
    def DialogPass():
        xbmc.sleep(75)
        if (xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
            while(xbmcgui.getCurrentWindowDialogId() == 10100) or (xbmcgui.getCurrentWindowDialogId() == 10101):
                xbmc.sleep(100)
            return True
        else:
            return False
    
    p1 = True
    p2 = True
    p3 = True
    p4 = True
    while(p1 or p2 or p3 or p4):
        p1 = DialogPass()
        p2 = DialogPass()
        p3 = DialogPass()
        p4 = DialogPass()

def InstallAddon(addon, xml):
    version = 0
    attempts = 0
    failed = False
    while (version == 0 and failed == False):
        DialogCheck()
        if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
            try:
                xbmc.executebuiltin('InstallAddon("' + addon + '")')
                attempts+=1
                if attempts == 10:
                    xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'failed to install: ' + str(addon))
                    failed = True
                    continue
            except:
                xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'failed to install: ' + str(addon))
                continue
        DialogCheck()
        if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
            if XMLExists(xml):
                try:
                    version = xbmcaddon.Addon(addon).getAddonInfo('version')
                    attempts+=1
                    if attempts == 10:
                        xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'failed to verify: ' + str(addon))
                        failed = True
                        continue
                except:
                    if (xbmcgui.getCurrentWindowDialogId() != 10100) and (xbmcgui.getCurrentWindowDialogId() != 10101):
                        xbmc.executebuiltin('EnableAddon("' + addon + '")')
                    if attempts == 10:
                        xbmcgui.Dialog().ok('[COLOR firebrick]Preloader[/COLOR]', 'failed to verify: ' + str(addon))
                        failed = True
                    continue

def XMLExists(pathaddon):
    return os.path.exists(pathaddon)

        
def ForceUpdate():
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('ReloadSkin(reload)')


def DownloadRepos(confirmedrepo, localrepos, reponamelist, repourllist):
    pathpackages = vars.PathPackages()                    
    for repo in confirmedrepo:
        if repo not in localrepos:
            if repo in reponamelist:
                try:
                    url = repourllist[reponamelist.index(repo)]
                    path = os.path.join(pathpackages, repo + '.zip')
                    request.urlretrieve(url, path)
                    ExtractRepo(path)
                    xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', repo + ' succesfully downloaded.')
                except HTTPError as error:
                    if error.code == 404:
                        xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', '[COLOR goldenrod][404][/COLOR] PAGE NOT FOUND')
                        xbmcgui.Dialog().ok('[COLOR goldenrod][ERROR 404][/COLOR]', 'Page not found, could not install.\n[REPO]: [COLOR firebrick]' + str(repo) + '[/COLOR]\nCheck ' + url)
                        exit()        

def CheckAvailability(addons, repos):
    localaddons, localrepos = vars.LocalAddons()
    addonnamelist = []
    addontypelist = []
    addonrepolist = []
    addondependencylist = []
    for addon in addons:
        addonnamelist.append(addon[0])
        addontypelist.append(addon[1])
        addonrepolist.append(addon[2])
        addondependencylist.append(addon[3])
        
    reponamelist = []
    repourllist = []
    for repo in repos:
        reponamelist.append(repo[0])
        repourllist.append(repo[1])
        
    i=0
    aa=0
    availableaddons = []
    availabletypes = []
    availablerepos = []
    availabledependencies = []
        

    for addonname in addonnamelist:
        if addonname not in localaddons:
            if addonrepolist[i] in reponamelist or addonrepolist[i] in localrepos or addonrepolist[i] is None:
                confirmdepends = 0
                for addondependency in addondependencylist[i]:
                    if addondependency not in addonnamelist and addondependency != [] and addondependencylist[i] != [] and addondependency not in localaddons:
                        confirmdepends = -1
                if confirmdepends == 0:
                    availableaddons.append(addonname)
                    availabletypes.append(addontypelist[i])
                    availablerepos.append(addonrepolist[i])
                    availabledependencies.append(addondependencylist[i])
                    aa+=1
        i+=1
        
    return addonnamelist, addontypelist, addonrepolist, addondependencylist, reponamelist, repourllist, availableaddons, availabletypes, availablerepos, availabledependencies

def SetupManager(currentAddons, availableaddons, currentDependencies, availabledependencies, currentRepos, availablerepos, currentTypes, availabletypes, types):
    setupselecter = 0
    
    while 'CONTINUE' not in types[setupselecter] and 'EXIT' not in types[setupselecter]:
        setupselecter = xbmcgui.Dialog().select('Setup Manager', types, 0, setupselecter, False)
        if setupselecter == -1:
            setup.init()
        if 'EXIT' in types[setupselecter]:
            CustomSetup()
        elif 'CONTINUE' in types[setupselecter]:
            return currentAddons, availableaddons, currentDependencies, availabledependencies, currentRepos, availablerepos, currentTypes, availabletypes
            
        tempAddons = []
        tempDependencies = []
        tempRepos = []
        tempTypes = []
        availabletopick = []
            
        i=0
        for addontype in availabletypes:
            available=1
            if addontype == types[setupselecter]:
                if currentDependencies != []:
                    for currentDependency in currentDependencies:
                        if availableaddons[i] in currentDependency:
                            available=-1
                    if available == 1:
                        availabletopick.append(availableaddons[i])
                else:
                    availabletopick.append(availableaddons[i])
            i+=1
                    
                
        currentAddonPicker = []
        if currentAddons != []:
            for currentAddon in currentAddons:
                if currentAddon in availabletopick:
                    currentAddonPicker.append(list(availabletopick).index(currentAddon))
        currentAddonPicker = xbmcgui.Dialog().multiselect(types[setupselecter], availabletopick, 0, currentAddonPicker)
        if currentAddonPicker is not None:
            for currentAddonPicked in currentAddonPicker:
                tempAddons.append(availabletopick[currentAddonPicked])
                i = availableaddons.index(availabletopick[currentAddonPicked])
                tempRepos.append(availablerepos[i])
                tempDependencies.append(availabledependencies[i])
                tempTypes.append(availabletypes[i])
                    

            for choice in availabletopick:
                if choice not in tempAddons:
                    if choice in currentAddons:
                        i = currentAddons.index(choice)
                        del currentAddons[i]
                        del currentDependencies[i]
                        del currentRepos[i]
                        del currentTypes[i]
                    
            i=0
            for tempAddon in tempAddons:
                if tempAddon not in currentAddons:
                    currentAddons.append(tempAddon)
                    currentRepos.append(tempRepos[i])
                    currentDependencies.append(tempDependencies[i])
                    currentTypes.append(tempTypes[i])
                i+=1

        continue

def CustomSetup():
    localaddons, localrepos = vars.LocalAddons()
    answer = dialog.AskCustomize()                 
    
    if answer == 'addons' or answer == 'repos':
        lists.Edit(answer)
    elif answer == 'quicksetup':
        types = vars.AddonTypes()
        types.append('[COLOR goldenrod]->[/COLOR] [COLOR firebrick]EXIT[/COLOR] [COLOR goldenrod]<-[/COLOR]')
        addons = lists.GetList('addons')
        repos = lists.GetList('repos')
        pathpackages = vars.PathPackages()
        
        addonnamelist, addontypelist, addonrepolist, addondependencylist, reponamelist, repourllist, availableaddons, availabletypes, availablerepos, availabledependencies = CheckAvailability(addons, repos)
        
        confirmedname = []
        confirmedtype = []
        confirmedrepo = []
        confirmeddependencies = []
        
        currentAddons = []
        currentDependencies = []
        currentRepos = []
        currentTypes = []
        
        currentAddons, availableaddons, currentDependencies, availabledependencies, currentRepos, availablerepos, currentTypes, availabletypes = SetupManager(currentAddons, availableaddons, currentDependencies, availabledependencies, currentRepos, availablerepos, currentTypes, availabletypes, types)
        
        if currentAddons is None or currentAddons == [] or currentAddons == False:
            CustomSetup()
        
        for currentAddon in currentAddons:
            i = addonnamelist.index(currentAddon)
            confirmedname.append(currentAddon)
            confirmedtype.append(addontypelist[i])
            confirmedrepo.append(addonrepolist[i])
            confirmeddependencies.append(addondependencylist[i])
            for depend in addondependencylist[i]:
                if depend not in confirmedname:
                    confirmedname.append(depend)
                    confirmedtype.append(addontypelist[addonnamelist.index(depend)])
                    confirmedrepo.append(addonrepolist[addonnamelist.index(depend)])
                    confirmeddependencies.append(addondependencylist[addonnamelist.index(depend)])
                

        addonpicked, addontype, temprepos, tempdepends = lists.MarkRequirements(confirmedname, confirmedtype, confirmedrepo, confirmeddependencies, -7)
        
        i=0
        configsum = ''
        for picked in addonpicked:
            if len(confirmedname) > 1:
                tempdepend = tempdepends[i]
                configsum = configsum + '[COLOR goldenrod][ADDON ID][/COLOR]: [COLOR limegreen]' + str(picked) + '[/COLOR]\n[COLOR goldenrod][TYPE][/COLOR]: [COLOR limegreen]' + str(addontype[i]) + '[/COLOR]\n[COLOR goldenrod][REPO][/COLOR]: ' + str(temprepos[i]) + '\n[COLOR goldenrod][DEPENDENCIES][/COLOR]: ' + str(tempdepend) + '\n\n'
                i+=1
            else:
                tempdepend = tempdepends
                configsum = configsum + '[COLOR goldenrod][ADDON ID][/COLOR]: [COLOR limegreen]' + str(picked) + '[/COLOR]\n[COLOR goldenrod][TYPE][/COLOR]: [COLOR limegreen]' + str(addontype[i]) + '[/COLOR]\n[COLOR goldenrod][REPO][/COLOR]: ' + str(temprepos[i]) + '\n[COLOR goldenrod][DEPENDENCIES][/COLOR]: ' + str(tempdepend) + '\n\n'

        skin = ''
        for addon in confirmedname:
            if 'skin.' in addon:
                skin = addon    
            
        xbmcgui.Dialog().textviewer('[COLOR firebrick]Install List[/COLOR]', configsum)
        
        finaldepends = []
        for depend in confirmeddependencies:
            if depend not in finaldepends:
                finaldepends.append(depend)
        finalname = []
        for name in confirmedname:
            if name not in finalname:
                finalname.append(name)
        
        DownloadRepos(confirmedrepo, localrepos, reponamelist, repourllist)        
        ForceUpdate()
        InstallAddons(list(set(confirmedrepo)))
        InstallAddons(confirmeddependencies)
        InstallAddons(confirmedname)
        vars.SetLang()
        # vars.SetMainPlayer(mainvideoplayer)
        if skin != '':
            vars.SetSkin(skin)
        
    elif answer == -1:
        init()
        
def PresetSetup():
    localaddons, localrepos = vars.LocalAddons()
    preset = dialog.ChoosePreset()
    profile, addonsxml, reposxml = dialog.ChooseProfile(preset)
    addons, repos = lists.GetList('preset', addons=addonsxml, repos=reposxml)
    
    addonnamelist = []
    addontypelist = []
    addonrepolist = []
    addondependencylist = []
    for addon in addons:
        addonnamelist.append(addon[0])
        addontypelist.append(addon[1])
        addonrepolist.append(addon[2])
        addondependencylist.append(addon[3])
        
    reponamelist = []
    repourllist = []
    for repo in repos:
        reponamelist.append(repo[0])
        repourllist.append(repo[1])
        
    i=0
    enable = True
    for addondependencies in addondependencylist:
        if addondependencies != [] and addondependencies is not None:
            for dependency in addondependencies:
                if dependency not in addonnamelist and dependency not in localaddons:
                    enable = False
            if not enable:
                del addonnamelist[i]
                del addontypelist[i]
                del addonrepolist[i]
                del addondependencylist[i]
        i+=1
    
    i=0
    enable=True
    for repo in addonrepolist:
        if repo != [] and repo is not None:
            if repo not in reponamelist and repo not in localrepos:
                enable = False
            if not enable:
                del addonnamelist[i]
                del addontypelist[i]
                del addonrepolist[i]
                del addondependencylist[i]
        i+=1
        
    types = ['script', 'movie provider', 'anime provider', 'tracking provider', 'widget', 'resource', vars.Buttons.btn_continue]
    currentAddons = addonnamelist
    currentDependencies = addondependencylist
    currentRepos = addonrepolist
    currentTypes = addontypelist
    addons = lists.GetList('addons')
    repos = lists.GetList('repos')
    addonnamelist, addontypelist, addonrepolist, addondependencylist, reponamelist, repourllist, availableaddons, availabletypes, availablerepos, availabledependencies = CheckAvailability(addons,repos)
    currentAddons, availableaddons, currentDependencies, availabledependencies, currentRepos, availablerepos, currentTypes, availabletypes = SetupManager(currentAddons, availableaddons, currentDependencies, availabledependencies, currentRepos, availablerepos, currentTypes, availabletypes, types)
        
    if addonnamelist is None or addonnamelist == [] or addonnamelist == False:
        PresetSetup()
        
    confirmedname = []  
    confirmedtype = []
    confirmedrepo = []
    confirmeddependencies = []
    for currentAddon in currentAddons:
        if currentAddon not in localaddons:
            i = addonnamelist.index(currentAddon)
            confirmedname.append(currentAddon)
            confirmedtype.append(addontypelist[i])
            confirmedrepo.append(addonrepolist[i])
            confirmeddependencies.append([confirmeddependency for confirmeddependency in addondependencylist[i]])
            for depend in addondependencylist[i]:
                if depend not in confirmedname:
                    confirmedname.append(depend)
                    confirmedtype.append(addontypelist[addonnamelist.index(depend)])
                    confirmedrepo.append(addonrepolist[addonnamelist.index(depend)])
                    confirmeddependencies.append(addondependencylist[addonnamelist.index(depend)])
            
    optionals = dialog.ChooseOptionals(confirmedname, confirmeddependencies)
    
    addonpicked, addontype, temprepos, tempdepends = lists.MarkRequirements(confirmedname, confirmedtype, confirmedrepo, confirmeddependencies, -7, addons=addonsxml, repos=reposxml)    
    
    i=0
    configsum = ''
    for picked in addonpicked:
        tempdepend = tempdepends[i]
        temprepo = temprepos[i]
        if temprepo == []: temprepo = None
        if tempdepend == []: tempdepend = None
        configsum = configsum + '[COLOR goldenrod][ADDON ID][/COLOR]: [COLOR limegreen]' + str(picked) + '[/COLOR]\n[COLOR goldenrod][TYPE][/COLOR]: [COLOR limegreen]' + str(addontype[i]) + '[/COLOR]\n[COLOR goldenrod][REPO][/COLOR]: ' + str(temprepo) + '\n[COLOR goldenrod][DEPENDENCIES][/COLOR]: ' + str(tempdepend) + '\n\n'
        i+=1
            
    xbmcgui.Dialog().textviewer('[COLOR firebrick]Install List[/COLOR]', configsum)
    
    finaldepends = []
    for depend in confirmeddependencies:
        if depend not in finaldepends:
            finaldepends.append(depend)
    finalname = []
    for name in confirmedname:
        if name not in finalname:
            finalname.append(name)
        
    DownloadRepos(list(set(confirmedrepo)), localrepos, reponamelist, repourllist)        
    ForceUpdate()
    InstallAddons(list(set(confirmedrepo)))
    InstallAddons(finaldepends)
    InstallAddons(finalname)
    ExtractPreset(preset, profile)
    ExtractOptionals(optionals)
    vars.SetLang()
    # vars.SetMainPlayer(mainvideoplayer)
    vars.SetSkin(preset.replace('.zip', ''))
    
def ExtractPreset(preset, profile):
    pathpresets = vars.PathPresets()
    pathkodi = vars.PathKodi()
    presetpath = os.path.join(pathpresets, preset)
    overwritten = 0
    extracted = 0
    details = []
    if os.path.exists(presetpath):
        from zipfile import ZipFile
        with ZipFile(presetpath, mode='r') as setup:
            for file in setup.namelist():
                if file.startswith(profile):
                    newname = file.replace(profile, '')
                    path = os.path.join(pathkodi, newname)
                    if os.path.exists(path) or os.path.isfile(path):
                        try:
                            if os.path.isdir(path) == False:
                                os.remove(path)
                                setup.getinfo(file).filename = newname
                                setup.extract(file, pathkodi)
                                details.append('Overwritten: ' + file)
                                overwritten+=1
                        except:
                            details.append(file + ' is being used by another process (Kodi)')
                    else:
                        setup.getinfo(file).filename = newname
                        setup.extract(file, pathkodi)
                        details.append('Extracted: ' + file)
                        extracted+=1
        
def ExtractOptionals(optionals):
    pathpresets = vars.PathPresets()
    pathkodi = vars.PathKodi()
    optionalzip = os.path.join(pathpresets, 'optionals.zip')
    overwritten = 0
    extracted = 0
    details = []
    if os.path.exists(optionalzip):
        from zipfile import ZipFile
        with ZipFile(optionalzip, mode='r') as setup:
            list = [file for option in optionals for file in setup.namelist() if option in file]
            for item in list:
                path = os.path.join(pathkodi, item)
                if os.path.exists(path) or os.path.isfile(path):
                    try:
                        if os.path.isdir(path) == False:
                            os.remove(path)
                            setup.extract(item, pathkodi)
                            details.append('Overwritten: ' + item)
                            overwritten+=1
                    except:
                        details.append(item + ' is being used by another process (Kodi)')
                else:
                    setup.extract(item, pathkodi)
                    details.append('Extracted: ' + item)
                    extracted+=1
    
    
    
            
def ExtractRepo(zip):
    pathaddons = vars.PathAddons()
    addon = str(zip).split(os.sep)[-1]
    overwritten = 0
    extracted = 0
    details = []
    from zipfile import ZipFile
    with ZipFile(zip) as setup:
        for item in setup.namelist():
            path = os.path.join(pathaddons, item)
            if os.path.exists(path) or os.path.isfile(path):
                try:
                    if os.path.isdir(path) == False:
                        os.remove(path)
                        setup.extract(item, pathaddons)
                        details.append('Overwritten: ' + item)
                        overwritten+=1
                except:
                    details.append(item + ' is being used by another process (Kodi)')
            else:
                setup.extract(item, pathaddons)
                details.append('Extracted: ' + item)
                extracted+=1
    
    if addon == 'skin.arctic.horizon.2.zip':
        for dir in os.listdir(pathaddons):
            if 'skin.arctic.horizon.2' in dir and dir != 'skin.arctic.horizon.2':
                oldpath = os.path.join(pathaddons, dir)
                destroypath = os.path.join(pathaddons, dir + '_old')
                newpath = os.path.join(pathaddons, 'skin.arctic.horizon.2')
                if os.path.exists(newpath):
                    os.rename(newpath, destroypath)
                    try:
                        os.remove(destroypath)
                    except:
                        print('Permission error: ' + str(destroypath))
                os.rename(oldpath, newpath)
                vars.ah2xbmcversion()
                    
    print('Setup succesful.\n' + str(overwritten) + ' items overwritten.\n')
    print('Setup succesful.\n' + str(extracted) + ' new items extracted.\n')
    xbmcgui.Dialog().textviewer('[COLOR firebrick]SETUP SUCCESS[/COLOR]', str(overwritten) + ' items overwritten.\n' + str(extracted) + ' new items extracted.')