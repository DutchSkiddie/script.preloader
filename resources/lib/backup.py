import os
import xbmcaddon
import xbmcgui
from datetime import datetime
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from resources.lib import dialog
from resources.lib import vars
from resources.lib import setup
from resources.lib import lists

def init():
    response = dialog.Backup()
    if response == 'savefiles':
        SaveBackup(response)
    elif response == 'saveconfig':
        SaveBackup(response)
    elif response.endswith('.zip'):
        LoadBackup(response)
    elif response == -1:
        exit()

def SaveBackup(savetype):
    def PickAddons():
        types = ['skin', 'script', 'movie provider', 'anime provider', 'tracking provider', 'widget', 'resource', 'video plugin', vars.Buttons.btn_continue]    
        pickingAddons = True
        response = 0
        while pickingAddons == True:
            tempAddons = []
            response = xbmcgui.Dialog().select('Backup Manager\t [COLOR goldenrod][TYPES][/COLOR]', types, 0, response, False)
            if response == -1:
                pickingAddons = False
                init()
            elif 'CONTINUE' in types[response]:
                types.remove(types[response])
                pickingAddons = False
                continue
            else:
                availableaddons = []
                i=0
                for type in addontype:
                    if type == types[response]:
                        availableaddons.append(addonname[i])
                    i+=1
                ci=[]
                for addon in availableaddons:
                    if addon in confirmedaddons:
                        ci.append(availableaddons.index(addon))
                i=0
                for type in addontypelist:
                    if type == types[response]:
                        if addonnamelist[i] not in availableaddons:
                            availableaddons.append(addonnamelist[i])
                    i+=1
            tempchoices = xbmcgui.Dialog().multiselect(types[response], availableaddons, 0, ci)
            if tempchoices is None:
                continue
            for choice in tempchoices:
                tempAddons.append(availableaddons[choice])
            for addon in availableaddons:
                if addon in confirmedaddons and addon not in tempAddons:
                    confirmedaddons.remove(addon)
                elif addon in tempAddons and addon not in confirmedaddons:
                    confirmedaddons.append(addon)
            continue
            
    def PickRepos():
        tempRepos = []
        repos = []
        cr=[]
        for repo in reponame:
            i = reponame.index(repo)
            if repourl[i] != None:
                repos.append('[COLOR limegreen]' + repo + '[/COLOR]')
            else:
                repos.append(repo)
            cr = [repos.index(repo) for repo in repos for confirmedrepo in confirmedrepos if confirmedrepo in repo]
        responses = xbmcgui.Dialog().multiselect('Backup Manager\t [COLOR goldenrod][REPOS][/COLOR]', repos, 0, cr)
        if responses == -1:
            init()
        else:
            for response in responses:
                tempRepos.append(reponame[response])
            for repo in reponame:
                if repo in confirmedrepos and repo not in tempRepos:
                    confirmedrepos.remove(repo)
                elif repo in tempRepos and repo not in confirmedrepos:
                    confirmedrepos.append(repo)
                
    
    def PickOptionals():
        pathaddondata = vars.PathAddondata()
        optionals = ['[COLOR firebrick]OVERWRITE[/COLOR] [COLOR goldenrod]' + optional + '[/COLOR]' for optional in confirmedaddons for file in os.listdir(pathaddondata) if optional in file]
        currentoptionals = list(range(0, len(optionals), 1))
        responses = xbmcgui.Dialog().multiselect('Backup Manager\t [COLOR goldenrod][OPTIONALS][/COLOR]', optionals, 0, currentoptionals)
        if responses == -1:
            init()
        else:
            tempoptionals = [optionals[response] for response in responses]
            for optional in tempoptionals:
                optional = str(optional).replace('[COLOR firebrick]OVERWRITE[/COLOR] [COLOR goldenrod]', '').replace('[/COLOR]', '')
                confirmedoptionals.append(optional)
    
    def ReposToXML():
        options = ET.Element('options')            
        i=0
        for repo in confirmedrepos:
            i = reponame.index(repo)
            repo = ET.SubElement(options, 'repo', name=repo)
            if repourl[i] is not None:
                url = repourl[i]
                ET.SubElement(repo, 'url').text = url
            i+=1
        del i

        tree = ET.ElementTree(options)
        return tree
            
            
    def AddonsToXML():    
        options = ET.Element('options')        
        for name in addonname:
            addon = ET.SubElement(options, 'addon', name=name)
            i = addonname.index(name)
            ET.SubElement(addon, 'type').text = addontype[i]
            ET.SubElement(addon, 'repo').text = addonrepo[i]
            dependencies = ET.SubElement(addon, 'dependencies')
            if addondepends[i] != [] and addondepends[i] is not None:
                for dependencyitem in addondepends[i]:
                    if isinstance(dependencyitem, (list, tuple)) and len(dependencyitem) > 1:
                        for dependency in dependencyitem:
                            if isinstance(dependency, (list, tuple)) and len(dependency) > 1:
                                for dep in dependency:
                                    ET.SubElement(dependencies, 'dependency').text = str(dep)
                            else:
                                ET.SubElement(dependencies, 'dependency').text = str(dependency)
                    elif isinstance(dependencyitem, (list, tuple)):
                        for dependency in dependencyitem:
                            if isinstance(dependency, (list, tuple)):
                                for dep in dependency:
                                    ET.SubElement(dependencies, 'dependency').text = str(dep)
                            else:
                                ET.SubElement(dependencies, 'dependency').text = str(dependency)              
                    else:
                        ET.SubElement(dependencies, 'dependency').text = str(dependencyitem)        
        tree = ET.ElementTree(options)
        return tree
                            
    def startSaving():
        pathaddons = vars.PathAddons()
        pathkodi = vars.PathKodi()
        pathaddondata = vars.PathAddondata()
        pathbackup = os.path.normpath(vars.PathBackups())
        if os.path.exists(pathbackup) == False and os.path.isdir(pathbackup) == False: 
            os.makedirs(pathbackup)
        repotree = ReposToXML()
        addontree = AddonsToXML()
        now = datetime.now()
        now = str(now).replace(' ', '_').replace(':', '.')
        skin = vars.GetSkin()
        
        if savetype == 'savefiles':
            pathzip = os.path.join(pathbackup, str(skin) + '_full_' + now + '.zip')

            with ZipFile(pathzip, 'w') as backup:
                addonfiles = [os.path.join(root, file) for root, dirs, files in os.walk(pathaddons) for addonPicked in confirmedaddons for file in files if addonPicked in root]
                for file in addonfiles:
                    backup.write(file, os.path.relpath(file, pathkodi))
                repofiles = [os.path.join(root, file) for root, dirs, files in os.walk(pathaddons) for repoPicked in confirmedrepos for file in files if repoPicked in root]   
                for file in repofiles:
                    backup.write(file, os.path.relpath(file, pathkodi))
                optionalfiles = [os.path.join(root, file) for root, dirs, files in os.walk(pathaddondata) for optionalPicked in confirmedoptionals for file in files if optionalPicked in root and 'backup' not in root]
                for file in optionalfiles:
                    backup.write(file, os.path.relpath(file, pathkodi))
                with backup.open('repos.xml', 'w') as writeobject:
                    repotree.write(writeobject, encoding='UTF-8', xml_declaration=True)
                with backup.open('addons.xml', 'w') as writeobject:
                    addontree.write(writeobject, encoding='UTF-8', xml_declaration=True)               
            backup.close()                
    
    
        elif savetype == 'saveconfig':
            pathzip = os.path.join(pathbackup, str(skin) + '_config_' + now + '.zip')            
            
            with ZipFile(pathzip, 'w') as backup:
                repofiles = [os.path.join(root, file) for root, dirs, files in os.walk(pathaddons) for repo in confirmedrepos for file in files if repo in root and repourl[reponame.index(repo)] is None]
                for repo in repofiles:
                    backup.write(repo, os.path.relpath(repo, pathkodi))
                optionalfiles = [os.path.join(root, file) for root, dirs, files in os.walk(pathaddondata) for optionalPicked in confirmedoptionals for file in files if optionalPicked in root and 'backup' not in root]
                for optional in optionalfiles:
                    backup.write(optional, os.path.relpath(optional, pathkodi))
                with backup.open('repos.xml', 'w') as writeobject:
                    repotree.write(writeobject, encoding='UTF-8', xml_declaration=True)
                with backup.open('addons.xml', 'w') as writeobject:
                    addontree.write(writeobject, encoding='UTF-8', xml_declaration=True)
            backup.close()
    
    localaddons, localrepos = vars.LocalAddons()
    addonnamelist, addontypelist, addonrepolist, addondependencylist, reponamelist, repourllist = configitems()
    
    addonname = []
    addontype = []
    addonrepo = []
    addondepends = []
    
    reponame = []
    repourl = []
    
    confirmedaddons=[]
    for addon in localaddons:
        addonname.append(addon)
        if addon in addonnamelist:
            i = addonnamelist.index(addon)
            addontype.append(addontypelist[i])
            addonrepo.append(addonrepolist[i])
            depends = []
            if addondependencylist[i] != [] and addondependencylist[i] is not None:
                for depend in addondependencylist[i]:
                    depends.append(depend)
            addondepends.append(depends)
        else:
            addontype.append(getType(addon))
            addonrepo.append(None)
            addondepends.append(getDepends(addon))
        confirmedaddons.append(addon)
    
    
    confirmedrepos=[]    
    for repo in localrepos:
        reponame.append(repo)
        if repo in reponamelist:
            i = reponamelist.index(repo)
            repourl.append(repourllist[i])
        else:
            repourl.append(None)
        confirmedrepos.append(repo)
    addonrepos = [addon for addon in confirmedaddons if addon in reponamelist]
    for addon in addonrepos:
        confirmedrepos.append(addon)
    configrepos = [repo for repo in reponamelist if repo not in localrepos]
    for repo in configrepos:
        reponame.append(repo)
        i = reponamelist.index(repo)
        repourl.append(repourllist[i])
        
    confirmedoptionals = []          
    
    PickAddons()
    PickRepos()
    PickOptionals()
    startSaving()
    doneb()    
    
def getType(addon):
    if 'skin' in addon:
        return 'skin'
    elif 'plugin.video' in addon:
        return 'video plugin'
    elif 'script.trakt' in addon:
        return 'tracking provider'
    elif 'script' in addon:
        return 'script'
    
def getDepends(addon):
    pathaddons = vars.PathAddons()
    path = os.path.join(pathaddons, addon)
    addonxml = os.path.join(path, 'addon.xml')
    if os.path.exists(addonxml) or os.path.isfile(addonxml):
        dependencies = []
        tree = ET.parse(addonxml)
        root = tree.getroot()
        if root.get('import') is not None:
            for dependency in root.findall('import'):
                dependencies.append(dependency.text)
        else:
            return None
    else:
        return None       
    
def configitems():
    addons = lists.GetList('addons')
    repos = lists.GetList('repos')
    
    addonnamelist=[]
    addontypelist=[]
    addonrepolist=[]
    addondependencylist=[]
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
        
    return addonnamelist, addontypelist, addonrepolist, addondependencylist, reponamelist, repourllist

def LoadBackup(backupzip):
    localaddons, localrepos = vars.LocalAddons()
    pathbackups = vars.PathBackups()
    pathkodi = vars.PathKodi()
    pathzip = os.path.normpath(os.path.join(pathbackups, backupzip))
    with ZipFile(pathzip) as checkup:
        addonfiles = [files for files in checkup.namelist() if files.startswith('addons') or files.startswith('userdata')]
        for file in addonfiles:
            pathfile = os.path.normpath(os.path.join(pathkodi, file))
            if os.path.exists(pathfile):
                try:
                    os.remove(pathfile)
                    checkup.extract(file, pathkodi)
                except:
                    print(file + 'is being used by another process (Kodi)')
            else:
                checkup.extract(file, pathkodi)
        addons = [files for files in checkup.namelist() if files.startswith('addons.xml')]
        repos = [files for files in checkup.namelist() if files.startswith('repos.xml')]
        for addon in addons:
            addonsxml = checkup.read(addon)
        for repo in repos:
            reposxml = checkup.read(repo)
        # reposxml = [files for files in checkup.namelist() if 'repos.xml' in os.path.relpath(files, pathkodi)]
    addons, repos = lists.GetList('backup', addons=addonsxml, repos=reposxml)
    
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
    
    currentAddons = addonnamelist
    currentDependencies = addondependencylist
    currentRepos = addonrepolist
    currentTypes = addontypelist
    
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
            confirmeddependency = []
            for depend in addondependencylist[i]:
                confirmeddependency.append(depend)
            confirmeddependencies.append(confirmeddependency)
            
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
      
    # setup.DownloadRepos(confirmedrepo, localrepos, reponamelist, repourllist)        
    setup.ForceUpdate()
    setup.InstallAddons(confirmedrepo)
    setup.InstallAddons(confirmeddependencies)
    setup.InstallAddons(confirmedname)
    setup.ExtractOptionals(optionals)
    vars.SetLang()
    # vars.SetMainPlayer(mainvideoplayer)
    vars.SetSkin(str(backupzip).split('_')[0])
        

def doneb():
    xbmcgui.Dialog().ok('[COLOR firebrick]SUCCESS[/COLOR]', 'BACKUP COMPLETE')