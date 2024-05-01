import xbmcgui
from resources.lib import sort
from resources.lib import vars

def CustomizeAddons(finalList, lastusedaddonconfig, pathkodi):
    genrelists = sort.sortAddons(finalList)
    
    skinpicked = []
    repospicked = []
    pluginspicked = []
    servicespicked = []
    scriptspicked = []
    
    skinslist = genrelists[0]
    repolist = genrelists[1]
    pluginlist = genrelists[2]
    servicelist = genrelists[3]
    scriptlist = genrelists[4]
    
    if not (lastusedaddonconfig):
        oldskin = sort.configitemreplace(vars.GetSkin())
        oldplugins = vars.GetPlugins(pathkodi)
        
    else:
        lastusedaddonconfig = str(lastusedaddonconfig).replace('["[', '').replace(']"]', '').replace("'", '').replace('" ', '"')
        lastusedaddonconfig = lastusedaddonconfig.split('", "')
        oldskin = lastusedaddonconfig[0]
        oldplugins = lastusedaddonconfig[1:]
    
    
    def SkinSelect(skinslist):
        try:
            iskin = skinslist.index(oldskin)
            skin = xbmcgui.Dialog().select('Pick a skin (Custom)', skinslist, 0, iskin, False)
        except:
            skin = xbmcgui.Dialog().select('Pick a skin (Custom)', skinslist, 0, 0, False)
        if(skin == -1):
            quit()
        else:
            return skin
    
    def PluginSelect(txt, list):
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
                return picker
        except:
            if (picker == None):
                quit()
            else:
                return picker
    
    skinpicker = SkinSelect(skinslist)
    repopicker = PluginSelect('Select your repos (Custom)', repolist)
    pluginpicker = PluginSelect('Choose your plugins (Custom)', pluginlist)
    servicepicker = PluginSelect('Decide your services (Custom)', servicelist)
    scriptpicker = PluginSelect('Designate scripts (Custom)', scriptlist)
    
    skinpicked = sort.reverseconfigitemreplace(skinslist[skinpicker])
    for choice in repopicker:
        repospicked.append(sort.reverseconfigitemreplace(repolist[choice]))
    for choice in pluginpicker:
        pluginspicked.append(sort.reverseconfigitemreplace(pluginlist[choice]))
    for choice in servicepicker:
        servicespicked.append(sort.reverseconfigitemreplace(servicelist[choice]))
    for choice in scriptpicker:
        scriptspicked.append(sort.reverseconfigitemreplace(scriptlist[choice]))
        
    plugins = []
    plugins.append(repospicked)
    plugins.append(pluginspicked)
    plugins.append(servicespicked)
    plugins.append(scriptspicked)
    
    config = []
    config.append(skinpicked)
    config.append(plugins)

    return config