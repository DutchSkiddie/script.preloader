import xbmcgui
import os
from resources.lib import sort
from resources.lib import vars
from resources.lib import dialog
from resources.lib import options
from resources.lib import lists


def CustomizeAddons(finalList, lastusedaddonconfig, setupchoice, pathpresets):
    genrelists = sort.sortAddons(finalList)
    
    mainskin = []
    mainvideoselect = ''
    skinpicked = []
    repospicked = []
    servicespicked = []
    scriptspicked = []
    
    skinslist = list(set(genrelists[0]))
    repolist = list(set(genrelists[1]))
    pluginlist = list(set(genrelists[2]))
    servicelist = list(set(genrelists[3]))
    scriptlist = list(set(genrelists[4]))
    
    
    if not (lastusedaddonconfig):
        oldplugins = vars.GetPlugins()
        
    else:
        lastusedaddonconfig = str(lastusedaddonconfig).replace('["[', '').replace(']"]', '').replace("'", '').replace('" ', '"')
        lastusedaddonconfig = lastusedaddonconfig.split('", "')
        oldplugins = lastusedaddonconfig[1:]
    
    def SingleSelect(txt, list):
        i = 0
        try:
            for config in lastusedaddonconfig:
                if (sort.configitemreplace(config) in list):
                    i = list.index(sort.configitemreplace(config))
            picker = xbmcgui.Dialog().select(txt, list, 0, i, False)
            if (picker == None):
                quit()
            else:
                return list[picker]
        except:
            if (picker == None):
                quit()
            else:
                return list[picker]
    
    def MultiSelect(txt, list):
        ilist = []
        c = 0
        try:
            for plugin in oldplugins:
                if(sort.configitemreplace(plugin) in list):
                    ilist.append(list.index(sort.configitemreplace(plugin)))
            if (ilist == []):
                for i in list:
                    ilist.append(c)
                    c+=1
            picker = xbmcgui.Dialog().multiselect(txt, list, 0, ilist, False)
            if (picker == None):
                quit()
            else:
                clist = []
                for i in picker:
                    clist.append(list[i])    
                return clist
        except:
            if (picker == None):
                quit()
            else:
                clist = []
                for i in picker:
                    clist.append(list[i])    
                return clist
    
    if (setupchoice != 3):
        skinpicker = SingleSelect('Pick a skin', list(set(skinslist)))
        skinpicked = sort.reverseconfigitemreplace(skinpicker)
        skinsselect = skinpicked
        pathskin = os.path.join(pathpresets, skinpicked + '.zip')
     
      
    if (setupchoice == 0):
        config = []
        config.append(skinslist)
        config.append(repolist)
        config.append(pluginlist)
        config.append(servicelist)
        config.append(scriptlist)           
        config = lists.chainlist(config)    
        
        for conf in config:
            i = config.index(conf)
            conf = sort.reverseconfigitemreplace(conf)
            config[i] = conf
        
        presetchoice = False
        repospicked = repolist
        mainskin = skinslist[0]
        repos = repolist
        addons = config
        depends = []
        repolist = []
        for repo in repos:
            repo = sort.configitemreplace(repo)
            repolist.append(repo)
        

    if (setupchoice == 1):
        presetchoice = dialog.ChoosePreset(pathskin)
        repos, addons = options.GetPresetOptions()
        depends = options.GetPresetDepends(skinpicked)
        optrepos = []
        optaddons = []
        movieproviderlist = []
        animeproviderlist = []
        trackingproviderlist = []
        movieproviders, animeproviders, trackingproviders, scripts, services = options.GetProviders()
        scriptlist = []
        servicelist = []
        
        for presetrepo in repos:
            if presetrepo not in depends:
                optrepos.append(presetrepo)
                    
        for addon in addons:
            if addon not in depends:
                optaddons.append(addon)
    
        newaddons = optrepos + optaddons
            
        for provider in movieproviders:
            if provider in newaddons:
                movieproviderlist.append(sort.configitemreplace(provider))
        for provider in animeproviders:
            if provider in newaddons:
                animeproviderlist.append(sort.configitemreplace(provider))
        for provider in trackingproviders:
            if provider in newaddons:
                trackingproviderlist.append(sort.configitemreplace(provider))
        for service in services:
            if service in newaddons:
                servicelist.append(sort.configitemreplace(service))
        for script in scripts:
            if script in newaddons:
                scriptlist.append(sort.configitemreplace(script))
        for repo in repolist:
            if repo in newaddons:
                repolist.append(sort.configitemreplace(repo))
                
                
        videoselect = MultiSelect('Select which provider(s) to use for movies and tv shows', list(set(movieproviderlist)))
        videospicked = []
        for video in videoselect:
            videodepends = options.GetPresetDepends(sort.reverseconfigitemreplace(video))
            for script in scriptlist:
                if sort.reverseconfigitemreplace(script) in videodepends:
                    scriptlist.remove(script)
                    videospicked.append(sort.reverseconfigitemreplace(script))
        if len(videoselect) > 1:
            usedefault = dialog.DefaultPlayer()
            if usedefault == True:
                mainvideoselect = sort.reverseconfigitemreplace(SingleSelect("[COLOR firebrick]DEFAULT PLAYER[/COLOR]", videoselect))        
            else:
                mainvideoselect = ''          
        animeselect = MultiSelect('Select which provider(s) to use for anime', list(set(animeproviderlist)))
        animespicked = []
        trackingselect = MultiSelect('Select which service(s) to use for tracking', list(set(trackingproviderlist)))
        trackingpicked = []
        scriptselect = MultiSelect('Pick additional script(s)', list(set(scriptlist)))
        scriptspicked = []
        serviceselect = MultiSelect('Choose added service(s)', list(set(servicelist)))
        servicespicked = []
        
        for choice in videoselect:
            videospicked.append(sort.reverseconfigitemreplace(choice))
        for choice in animeselect:
            animespicked.append(sort.reverseconfigitemreplace(choice))
        for choice in trackingselect:
            trackingpicked.append(sort.reverseconfigitemreplace(choice))
        for choice in serviceselect:
            servicespicked.append(sort.reverseconfigitemreplace(choice))
        for choice in scriptselect:
            scriptspicked.append(sort.reverseconfigitemreplace(choice))
            
        optionals = []
        optionals.append(videospicked)
        optionals.append(animespicked)
        optionals.append(trackingpicked)
        optionals.append(servicespicked)
        optionals.append(scriptspicked)
        
        currentAddons = []
        for i in depends:
            currentAddons.append(i)
        for i in lists.chainlist(optionals):
            currentAddons.append(i)
        currentAddons.append(skinpicked)
        
        currentAddons = list(set(currentAddons))
    
        reqrepos = list(set(options.GetPresetRepos(currentAddons)))
    
        extrarepos = []
        for repo in repolist:
            if sort.reverseconfigitemreplace(repo) not in reqrepos:
                extrarepos.append(sort.reverseconfigitemreplace(repo))
        reposelect = MultiSelect('Get more repos', extrarepos)
        repospicked = []
    
        for repo in reqrepos:
            repospicked.append(repo)
        for choice in reposelect:
            repospicked.append(sort.reverseconfigitemreplace(choice))
        
        repospicked = list(set(repospicked))

        config = []
        config.append(skinsselect)
        config.append(repospicked)
        config.append(depends)
        config.append(lists.chainlist(optionals))
    
    
    
        skin = config[:1]
        config = config[1:]    
        config = lists.chainlist(config)    
        config = skin + config
        
    else:
        newaddons = finalList
        presetchoice = False
    
    if (setupchoice == 3):
        presetchoice = False
        repos = vars.GetRepos()
        addons = vars.GetPlugins()
        depends = []
        repolist = []
        for repo in repos:
            repo = sort.configitemreplace(repo)
            repolist.append(repo)
            
        skinselect = []
        skinsselect = MultiSelect('Select which skin(s) to export', skinslist)
        if (len(skinsselect) > 1):
            skinselect = SingleSelect('Select which skin to use mainly', skinsselect)
            mainskin = sort.reverseconfigitemreplace(skinselect)
        else:
            mainskin = sort.reverseconfigitemreplace(str(skinsselect))
        for skin in skinsselect:
            i = skinsselect.index(skin)
            skin = sort.reverseconfigitemreplace(skin)
            skinsselect[i] = skin

        

        pluginselect = MultiSelect('Select which video plugin(s) to use', pluginlist)
        for plugin in pluginselect:
            i = pluginselect.index(plugin)
            plugin = sort.reverseconfigitemreplace(str(plugin))
            pluginselect[i] = plugin
        scriptselect = MultiSelect('Decide on which script(s) to include', scriptlist)
        for script in scriptselect:
            i = scriptselect.index(script)
            script = sort.reverseconfigitemreplace((script))
            scriptselect[i] = script
        serviceselect = MultiSelect('Choose alternate service(s)', servicelist)
        for service in serviceselect:
            i = serviceselect.index(service)
            service = sort.reverseconfigitemreplace((service))
            serviceselect[i] = service
        reposelect = MultiSelect('Select ALL required repos', repolist)
        for repo in reposelect:
            i = reposelect.index(repo)
            repo = sort.reverseconfigitemreplace((repo))
            reposelect[i] = repo
            
        repospicked = reposelect    
                
        config = []
        config.append(reposelect)
        config.append(pluginselect)
        config.append(scriptselect)
        config.append(serviceselect)
        config.insert(0,skinsselect)
        config = lists.chainlist(config)
        

    
    s = '[COLOR orange]CURRENT CONFIG: [/COLOR]\n\n'
    for i in config:
        s += '[COLOR lightseagreen]' + str(i) + '[/COLOR]' + '\n'
        
    xbmcgui.Dialog().textviewer('[COLOR firebrick]Preloader[/COLOR]', str(s))

    if (mainskin == []):
        mainskin = skinpicked

    return config, presetchoice, repospicked, mainskin, mainvideoselect