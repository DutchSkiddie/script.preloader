import os
import xbmc
import xbmcgui
from xml.etree import ElementTree as ET
from resources.lib import vars
from resources.lib import setup

def Flatten(list):
    return [item for listitem in list for item in listitem]

def MarkRequirements(namelist, typelist, repolist, dependencylist, picker, addons=None, repos=None):
    localaddons, localrepos = vars.LocalAddons()
    if repos is None:
        repos = GetList('repos')
    else:
        addons, repos = GetList('preset', addons=addons, repos=repos)
    reponamelist = []
    repourllist = []
    for repo in repos:
        reponamelist.append(repo[0])
        repourllist.append(repo[1])
    
    if picker != -7:
        addonpicked = namelist[picker]
        addontype = typelist[picker]
        addonrepos = repolist[picker]
        addondepends = dependencylist[picker]
    elif picker == -7:
        addonpicked = namelist
        addontype = typelist
        addonrepos = repolist
        addondepends = dependencylist
                   
    temprepos = []
    if isinstance(addonrepos, (list, tuple)):
        for repo in addonrepos:
            if repo is not None:
                if '[/COLOR]' not in repo:
                    if repo in localrepos or repo in reponamelist or picker == -7:
                        repo = '[COLOR limegreen]' + str(repo) + '[/COLOR]'
                        temprepos.append(repo)
                    else:
                        repo = '[COLOR firebrick]' + str(repo) + '[/COLOR]'
                        temprepos.append(repo)
            else:
                temprepos.append(repo)
                            
    if isinstance(addondepends, (list, tuple)):
        currentdepends = []
        if picker != -7:
            tempdepends = []
        for depend in addondepends:
            if picker == -7:
                tempdepends = []
            if depend is not None:
                if '[/COLOR]' not in depend:
                    if isinstance(depend, (list, tuple)):
                        for dep in depend:
                            if dep in localaddons or dep in namelist or picker == -7:
                                dep = '[COLOR limegreen]' + str(dep) + '[/COLOR]'
                                tempdepends.append(dep)
                            else:
                                dep = '[COLOR firebrick]' + str(dep) + '[/COLOR]'
                                tempdepends.append(dep)
                    else:
                        if depend in localaddons or depend in namelist:
                            depend = '[COLOR limegreen]' + str(depend) + '[/COLOR]'
                            tempdepends.append(depend)
                        else:
                            depend = '[COLOR firebrick]' + str(depend) + '[/COLOR]'
                            tempdepends.append(depend)
            currentdepends.append(tempdepends)
    
    if picker == -7:
        tempdepends = currentdepends                
    if tempdepends == []:
        tempdepends = 'None'
            
    return addonpicked, addontype, temprepos, tempdepends

def Edit(listtype):
    customlist = GetList(listtype)
    
    namelist = []
    typelist = []
    repolist = []
    dependencylist = []
    urllist = []
    
    def RemoveButtons(alist):
        newlist = []
        for item in alist:
            templist = []
            if len(item) > 1 and isinstance(item, (list, tuple)):
                for iitem in item:
                    if iitem:
                        if iitem != [[]] and iitem != []:
                            if '[/COLOR]' not in iitem:
                                templist.append(iitem)
                        else:
                            templist.append(None)
            elif item and item != [[]]:
                if '[/COLOR]' not in item:  
                    templist.append(item)
            else:
                templist.append(None)
            newlist.append(templist)
            del templist
        return newlist
    
    
    completed = False
    types = vars.AddonTypes()
    
    def KeyboardInput(alistitem, placeholder):
        if alistitem == '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]' or alistitem == '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD URL[/COLOR] [COLOR goldenrod]<-[/COLOR]':
            keyboard = xbmc.Keyboard(placeholder)
        else:
            keyboard = xbmc.Keyboard(alistitem)
        keyboard.doModal()
        if keyboard.isConfirmed():
            alistitem = keyboard.getText()
            return alistitem
    
    
    def EditDependencies():
        donepicking = False
        while donepicking == False:
            dependencypicker = xbmcgui.Dialog().select('[COLOR firebrick]DEPENDENCIES[/COLOR]', dependencylist[picker])
            if dependencypicker == -1 or str(dependencylist[picker][dependencypicker]) == vars.Buttons.btn_continue:
                donepicking = True
                continue
            else:
                if dependencylist[picker][dependencypicker] == '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]':
                    modifydependency = 2
                else:
                    modifydependency = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]EDIT[/COLOR]', dependencylist[picker][dependencypicker], 'EDIT', 'BACK', 'REMOVE')
                if modifydependency == -1 or modifydependency == 0:
                    continue
                elif modifydependency == 1:
                    confirmdelete = xbmcgui.Dialog().yesno('[COLOR gold]WARNING[/COLOR]', '[COLOR firebrick]Are you sure?[/COLOR]')
                    if confirmdelete == True:
                        temp = []
                        for dependency in dependencylist[picker]:
                            if '[/COLOR]' not in dependency and dependency != dependencylist[picker][dependencypicker]:
                                temp.append(dependency)
                        temp.append('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]')
                        temp.append(vars.Buttons.btn_continue)
                        
                        dependencylist[picker] = temp
                    continue
                elif modifydependency == 2:
                    dependencylist[picker][dependencypicker] = KeyboardInput(dependencylist[picker][dependencypicker], 'plugin.dependency')
                                
                    temp = []
                    for dependency in dependencylist[picker]:
                        temp.append(dependency)
                    if '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]' not in dependencylist[picker]:
                        temp.remove(vars.Buttons.btn_continue)
                        temp.append('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]')
                        temp.append(vars.Buttons.btn_continue)
                    dependencylist[picker] = temp
                    del temp
            continue
    
    def EditRepos():
        donepicking = False
        while donepicking == False:
            repopicker = xbmcgui.Dialog().select('[COLOR firebrick]REPO[/COLOR]', repolist[picker])
            if repopicker == -1 or repolist[picker][repopicker] == vars.Buttons.btn_continue:
                donepicking = True
                continue
            if repolist[picker][repopicker] == '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]':
                modifyrepo = 2
            else:
                modifyrepo = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]EDIT[/COLOR]', repolist[picker][repopicker], 'EDIT', 'BACK', 'REMOVE')
            if modifyrepo == -1 or modifyrepo == 0:
                continue
            elif modifyrepo == 1:
                confirmdelete = xbmcgui.Dialog().yesno('[COLOR gold]WARNING[/COLOR]', '[COLOR firebrick]Are you sure?[/COLOR]')
                if confirmdelete == True:
                    if repolist[picker][repopicker] != vars.Buttons.btn_continue:
                        repolist[picker][repopicker] = '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]'
                continue
            elif modifyrepo == 2:
                repolist[picker][repopicker] = KeyboardInput(repolist[picker][repopicker], 'repository.name')
    
    def EditName():
        addonname = namelist[picker]
        keyboard = xbmc.Keyboard(addonname, 'addon.id', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            namelist[picker] = keyboard.getText()
                
    def EditType():
        donepicking = False
        while donepicking == False:
            if typelist[picker] in types:
                i = types.index(typelist[picker])
            else:
                i = 0
            typeselect = xbmcgui.Dialog().select('[COLOR firebrick]TYPE[/COLOR]', types, 0, i)
            if typeselect == -1 or types[typeselect] == vars.Buttons.btn_continue:
                donepicking = True
                continue
            else:
                typelist[picker] = types[typeselect]
                continue
    
    def EditUrl():
        donepicking = False
        while donepicking == False:
            urlpicker = xbmcgui.Dialog().select('[COLOR firebrick]EDIT URL[/COLOR]', urllist[picker])
            if urlpicker == -1 or urllist[picker][urlpicker] == vars.Buttons.btn_continue:
                donepicking = True
                continue
            if urllist[picker][urlpicker] == '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD URL[/COLOR] [COLOR goldenrod]<-[/COLOR]':
                modifyrepo = 2
            else:
                modifyrepo = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]EDIT[/COLOR]', urllist[picker][urlpicker], 'EDIT', 'BACK', 'REMOVE')
            if modifyrepo == -1 or modifyrepo == 0:
                continue
            elif modifyrepo == 1:
                confirmdelete = xbmcgui.Dialog().yesno('[COLOR gold]WARNING[/COLOR]', '[COLOR firebrick]Are you sure?[/COLOR]')
                if confirmdelete == True:
                    if urllist[picker][urlpicker] != vars.Buttons.btn_continue:
                        urllist[picker][urlpicker] = '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD URL[/COLOR] [COLOR goldenrod]<-[/COLOR]'
                continue
            elif modifyrepo == 2:
                urllist[picker][urlpicker] = KeyboardInput(urllist[picker][urlpicker], 'https://example.com/example.zip')
    
    if listtype == 'addons':
        for addon in customlist:
            namelist.append(addon[0])
            typelist.append(addon[1])
            repolist.append([addon[2], vars.Buttons.btn_continue])
            tempdependencies = []
            for dependency in addon[3]:
                tempdependencies.append(dependency)
            tempdependencies.append('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]')
            tempdependencies.append(vars.Buttons.btn_continue)
            dependencylist.append(tempdependencies)
            
        namelist.append('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW ADDON[/COLOR] [COLOR goldenrod]<-[/COLOR]')
        typelist.append('skin')
        repolist.append(['[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]', vars.Buttons.btn_continue])
        dependencylist.append(['[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]', vars.Buttons.btn_continue])
        

        while completed == False:
            repos = GetList('repos')
            localaddons, localrepos = vars.LocalAddons()
            
            reponamelist = []
            repourllist = []
            for repo in repos:
                reponamelist.append(repo[0])
                repourllist.append(repo[1])
            
            i = namelist.index('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW ADDON[/COLOR] [COLOR goldenrod]<-[/COLOR]')
            picker = xbmcgui.Dialog().select('[COLOR firebrick]ADDONS[/COLOR]', namelist, 0, i)
            if picker == -1:
                list.pop(namelist)
                list.pop(typelist)
                list.pop(repolist)
                list.pop(dependencylist)
                SaveAddons(RemoveButtons(namelist), RemoveButtons(typelist), RemoveButtons(repolist), RemoveButtons(dependencylist))
                completed = True
                continue
            addonpicked = namelist[picker]
            
            if addonpicked == '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW ADDON[/COLOR] [COLOR goldenrod]<-[/COLOR]':
                    keyboard = xbmc.Keyboard('plugin.name', '[COLOR firebrick]NEW ADDON[/COLOR]', False)
                    keyboard.doModal()
                    if keyboard.isConfirmed():
                        namelist[picker] = keyboard.getText()
                        if '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW ADDON[/COLOR] [COLOR goldenrod]<-[/COLOR]' not in namelist:
                            namelist.append('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW ADDON[/COLOR] [COLOR goldenrod]<-[/COLOR]')
                            typelist.append('skin')
                            repolist.append(['[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]', vars.Buttons.btn_continue])
                            dependencylist.append(['[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD[/COLOR] [COLOR goldenrod]<-[/COLOR]', vars.Buttons.btn_continue])
                    EditType()
                    EditRepos()
                    EditDependencies()
                    continue
            else:
                editing = True
                while editing == True:
                    addonpicked, addontype, temprepos, tempdepends = MarkRequirements(namelist, typelist, repolist, dependencylist, picker)
                    response = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]EDIT[/COLOR]', '[COLOR goldenrod][ADDON ID][/COLOR]: [COLOR limegreen]' + str(addonpicked) + '[/COLOR]\n[COLOR goldenrod][ADDON TYPE][/COLOR]: [COLOR limegreen]' + str(addontype) + '[/COLOR]\n[COLOR goldenrod][SOURCE REPO][/COLOR]: ' + str(temprepos) + '\n[COLOR goldenrod][DEPENDENCIES][/COLOR]: ' + str(tempdepends), 'EDIT', 'BACK', 'REMOVE')
                    if response == -1 or response == 0:
                        editing = False
                        continue
                    if response == 1:
                        confirmdelete = xbmcgui.Dialog().yesno('[COLOR gold]WARNING[/COLOR]', '[COLOR firebrick]Are you sure?[/COLOR]')
                        if confirmdelete == True:
                            del namelist[picker]
                            del typelist[picker]
                            del repolist[picker]
                            del dependencylist[picker]
                            editing = False
                        continue
                    if response == 2:
                        editingattr = True
                        while editingattr == True:
                            addonpicked, addontype, temprepos, tempdepends = MarkRequirements(namelist, typelist, repolist, dependencylist, picker)
                            response = xbmcgui.Dialog().select('[COLOR firebrick]EDIT ADDON[/COLOR]', ["[COLOR goldenrod][ADDON ID][/COLOR]: [COLOR limegreen]" + str(addonpicked) + "[/COLOR]", "[COLOR goldenrod][ADDON TYPE][/COLOR]: [COLOR limegreen]" + str(addontype) + "[/COLOR]", "[COLOR goldenrod][SOURCE REPO][/COLOR]: " + str(temprepos), "[COLOR goldenrod][DEPENDENCIES][/COLOR]: " + str(tempdepends)])
                            if response == -1:
                                editingattr = False
                                continue
                            elif response == 0:
                                EditName()
                                continue
                            elif response == 1:
                                EditType()
                                continue
                            elif response == 2:
                                EditRepos()
                                continue
                            elif response == 3:
                                EditDependencies()
                                continue  
            continue
        
        
    elif listtype == 'repos':
        for repo in customlist:
            namelist.append(repo[0])
            urllist.append([repo[1], vars.Buttons.btn_continue])
            
        namelist.append('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW REPO[/COLOR] [COLOR goldenrod]<-[/COLOR]')
        urllist.append(['[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD URL[/COLOR] [COLOR goldenrod]<-[/COLOR]', vars.Buttons.btn_continue])
        

        while completed == False:
            i = namelist.index('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW REPO[/COLOR] [COLOR goldenrod]<-[/COLOR]')
            picker = xbmcgui.Dialog().select('[COLOR firebrick]REPOS[/COLOR]', namelist, 0, i)
            if picker == -1:
                SaveRepos(RemoveButtons(namelist), RemoveButtons(urllist))
                completed = True
                continue
            repopicked = namelist[picker]
            
            if repopicked == '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW REPO[/COLOR] [COLOR goldenrod]<-[/COLOR]':
                    keyboard = xbmc.Keyboard('repository.name', '', False)
                    keyboard.doModal()
                    if keyboard.isConfirmed():
                        namelist[picker] = keyboard.getText()
                        if '[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW REPO[/COLOR] [COLOR goldenrod]<-[/COLOR]' not in namelist:
                            namelist.append('[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]NEW REPO[/COLOR] [COLOR goldenrod]<-[/COLOR]')
                            urllist.append(['[COLOR goldenrod]->[/COLOR] [COLOR mediumturquoise]ADD URL[/COLOR] [COLOR goldenrod]<-[/COLOR]', vars.Buttons.btn_continue])
                    EditUrl()
                    continue
            else:
                editing = True
                while editing == True:
                    repopicked = namelist[picker]
                    response = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]EDIT[/COLOR]', '[COLOR goldenrod][ADDON ID][/COLOR]: [COLOR limegreen]' + str(repopicked) + '[/COLOR]', 'EDIT', 'BACK', 'REMOVE')
                    if response == -1 or response == 0:
                        editing = False
                        continue
                    if response == 1:
                        confirmdelete = xbmcgui.Dialog().yesno('[COLOR gold]WARNING[/COLOR]', '[COLOR firebrick]Are you sure?[/COLOR]')
                        if confirmdelete == True:
                            del namelist[picker]
                            del urllist[picker]
                            editing = False
                        continue
                    if response == 2:
                        addonurl = urllist[picker]
                        tempurl = []
                        for url in addonurl:
                            if url is not None:
                                if '[/COLOR]' not in url:
                                    tempurl.append(url)
                            if tempurl == []:
                                tempurl = 'None'                        
                        
                        response = xbmcgui.Dialog().yesnocustom('[COLOR firebrick]' + str(repopicked) + '[/COLOR]', '[COLOR goldenrod][SOURCE URL][/COLOR]: [COLOR limegreen]' + str(tempurl) + '[/COLOR]', 'URL', 'BACK', 'NAME')
                        if response == -1 or response == 0:
                            continue
                        elif response == 1:
                            reponame = namelist[picker]
                            keyboard = xbmc.Keyboard(reponame, 'repository.name', False)
                            keyboard.doModal()
                            if keyboard.isConfirmed():
                                namelist[picker] = keyboard.getText()
                            continue
                        elif response == 2:
                                EditUrl()
                                continue

                  
            continue
    setup.init()
    
def SaveRepos(namelist, urllist):
    userdatapath = vars.PathAddonUserdata()
    xmlpath = os.path.join(userdatapath, 'repos.xml')
    options = ET.Element('options')
    
    i=0
    names = [str(name).split("'")[1] for name in namelist if name != []]
    for name in names:
        repo = ET.SubElement(options, 'repo', name=name)
        if urllist[i] != []:
            url = str(urllist[i]).split("'")[1]
            ET.SubElement(repo, 'url').text= url
        i+=1
    del i

    tree = ET.ElementTree(options)
    if os.path.exists(os.path.dirname(xmlpath)) or os.path.isfile(xmlpath):
        tree.write(xmlpath)
    else:
        os.mkdir(os.path.dirname(xmlpath))
        tree.write(xmlpath)
    
    
def SaveAddons(namelist, typelist, repolist, dependencylist):
    userdatapath = vars.PathAddonUserdata()
    xmlpath = os.path.join(userdatapath, 'addons.xml')
    options = ET.Element('options')
    
    i=0
    for name in namelist:
        name = str(name).replace("['", '').replace("']", '')
        type = str(typelist[i]).replace("['", '').replace("']", '')
        repo = str(repolist[i]).replace("['", '').replace("']", '').replace('[]', '')
        addon = ET.SubElement(options, 'addon', name=name)
        ET.SubElement(addon, 'type').text = type
        ET.SubElement(addon, 'repo').text = repo
        dependencies = ET.SubElement(addon, 'dependencies')
        for dependencyitem in dependencylist[i]:
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
        i+=1
    del i

    tree = ET.ElementTree(options)
    if os.path.exists(os.path.dirname(xmlpath)) or os.path.isfile(xmlpath):
        tree.write(xmlpath)
    else:
        os.mkdir(os.path.dirname(xmlpath))
        tree.write(xmlpath)
    
def GetList(listtype, addons=None, repos=None):
    def returnList(xml, type):
        if listtype != 'preset' and listtype != 'optionals' and listtype != 'backup':
            tree = ET.parse(xml)
            root = tree.getroot()
        else:
            root = ET.fromstring(xml)
            
        list = []
        if type == 'addons':
            for addon in root.findall('addon'):
                name = addon.get('name')
                type = addon.find('type').text
                repo = addon.find('repo').text
                dependencies = []
                for dependency in addon.findall('.//dependency'):
                    dependencies.append(dependency.text)
                                    
                temp = []
                temp.append(name)
                temp.append(type)
                temp.append(repo)
                temp.append(dependencies)
                
                list.append(temp)
                del temp
                del dependencies
        if type == 'repos':
            for repo in root.findall('repo'):
                name = repo.get('name')
                if repo.find('url') is not None and repo.find('url').text is not None:
                    url = repo.find('url').text
                
                temp = []
                temp.append(name)
                if 'url' in locals(): temp.append(url)
                if 'url' not in locals(): temp.append(None)
                list.append(temp)
                if 'url' in locals(): del url
                del temp
        return list
    
    if listtype == 'optionals':
        xmlname = 'optionals.xml'
    elif listtype == 'addons':
        xmlname = 'addons.xml'
        type = 'addons'
    elif listtype == 'repos':
        xmlname = 'repos.xml'
        type = 'repos'
        
    userdatapath = vars.PathAddonUserdata()
    custompath = vars.PathCustom()
    presetpath = vars.PathPresets()
        
    if listtype == 'addons' or listtype == 'repos':
        userdataxml = os.path.join(userdatapath, xmlname)
        addonxml = os.path.join(custompath, xmlname)
        if os.path.isfile(userdataxml):
            addons = returnList(userdataxml, type)
            return addons
        elif os.path.isfile(addonxml):
            addons = returnList(addonxml, type)
            return addons
        else:
            xbmcgui.Dialog().ok('[COLOR gold]ERROR[/COLOR]', 'NO XML FOUND')
            return []
    elif listtype == 'preset':
        addons = returnList(addons, 'addons')
        repos = returnList(repos, 'repos')
        return addons, repos
    elif listtype == 'optionals':
        addons = returnList(addons, 'addons')
        repos = returnList(repos, 'repos')
        return addons, repos
    elif listtype == 'backup':
        addons = returnList(addons, 'addons')
        repos = returnList(repos, 'repos')
        return addons, repos