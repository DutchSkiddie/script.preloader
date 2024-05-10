from resources.lib import lists

def sortAddons(list):
    order = ["SKIN:", "REPO:", "PLUGIN:", "SERVICE:", "SCRIPT: "]
    newlist = []
    skinslist = []
    repolist = []
    pluginlist = []
    servicelist = []
    scriptlist = []
        
    for listitem in list:
        if order[0] in listitem:
            skinslist.append(listitem)
        if order[1] in listitem:
            repolist.append(listitem)
        if order[2] in listitem:
            pluginlist.append(listitem)
        if order[3] in listitem:
            servicelist.append(listitem)
        if order[4] in listitem:
            scriptlist.append(listitem)
        
    newlist.append(skinslist)
    newlist.append(repolist)
    newlist.append(pluginlist)
    newlist.append(servicelist) 
    newlist.append(scriptlist)
       
    return newlist
 
def configitemreplace(configitem):
        configitem = configitem.title()
        configitem = configitem.replace('Plugin.Video.', 'VIDEO PLUGIN: ')
        configitem = configitem.replace('Repository.', 'REPO: ')
        configitem = configitem.replace('Script.', 'SCRIPT: ')
        configitem = configitem.replace('Service.', 'SERVICE: ')
        configitem = configitem.replace('Skin.', 'SKIN: ')
        configitem = configitem.replace('.', ' ')
        return configitem
        
def reverseconfigitemreplace(configitem):
    configitem = configitem.replace('VIDEO PLUGIN: ', 'plugin.video.')
    configitem = configitem.replace('REPO: ', 'repository.')
    configitem = configitem.replace('SCRIPT: ', 'script.')
    configitem = configitem.replace('SERVICE: ', 'service.')
    configitem = configitem.replace('SKIN: ', 'skin.')
    configitem = configitem.replace(' ', '.')
    configitem = configitem.lower()
    return configitem

def FilterAddons(newaddonconfignames, lastusedaddonconfig):
    finalList = []
    lastUsedConfig = []
    for configitem in newaddonconfignames:
        if (configitem.startswith('context') or configitem.startswith('resource') or configitem.startswith('script.module')) == False:
            configitem = configitemreplace(configitem)
            finalList.append(configitem)
    
    
    # if not lastusedaddonconfig:        
    for configitem in lastusedaddonconfig:
        if (configitem.startswith('context') or configitem.startswith('resource') or configitem.startswith('script.module')) == False:
            configitem = configitemreplace(configitem)
            lastUsedConfig.append(configitem)

    finalList = sortAddons(finalList)
    lastUsedConfig = sortAddons(lastUsedConfig)
    
    
    finalList = lists.chainlist(finalList)
    lastUsedConfig = [val for sublist in lastUsedConfig for val in sublist]
    
    return finalList, lastUsedConfig