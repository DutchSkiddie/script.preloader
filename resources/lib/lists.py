import os
from resources.lib import custom
from resources.lib import sort
from resources.lib import options
from resources.lib import vars

def AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi, pathpresets):
    newaddonlist = []
    newaddonconfignames = []
    configlistnames = []
    finalList = []
    
    if(lastusedaddonconfigtxt != ''):
        lastusedaddonconfig = lastusedaddonconfigtxt.split(',')
    else:
        lastusedaddonconfig = []
    
    if (setupchoice == 0):
        from zipfile import ZipFile
        with ZipFile(zip) as compare1:
            newaddons = compare1.namelist()
    if (setupchoice == 1):
        repolist, addonlist = options.GetPresetOptions()
        newaddons = repolist + addonlist
    if (setupchoice == 2) or (setupchoice == 3):
        newaddons = os.listdir(os.path.join(pathkodi, 'addons'))       
    
    if (setupchoice == 0):
        for configitem in newaddons:
            if (configitem.startswith('addons') and (configitem.startswith('addons/packages/') == False)) and (configitem.endswith('addon.xml')):
                aoname = configitem.split('/')[1]
                newaddonconfignames.append(aoname)
                newaddonlist.append(configitem)
    if (setupchoice == 1):
        for configitem in newaddons:
            newaddonconfignames.append(configitem)
            newaddonlist.append(configitem)
    if (setupchoice == 2) or (setupchoice == 3):
        for configitem in newaddons:
            if ((configitem.startswith('packages') == False)):
                newaddonconfignames.append(configitem)
                newaddonlist.append(configitem)

    
    if(str(newaddons) == str(lastusedaddons)):        
        finalList, lastUsedConfig = sort.FilterAddons(newaddonconfignames, lastusedaddonconfig)   
                
    else:
        finalList, lastUsedConfig = sort.FilterAddons(newaddonconfignames, lastusedaddonconfig)         
    
    
    if (setupchoice == 0) or (setupchoice == 1) or (setupchoice == 3):
        configlistnames, presetchoice, repos, mainskin = (custom.CustomizeAddons(finalList, lastusedaddonconfig, setupchoice))         
    if (setupchoice == 2):
        presetchoice = []
        temp = []
        repos = vars.GetRepos()
        configlistnames, lastused = sort.FilterAddons(newaddonconfignames, lastUsedConfig)
        for configlistname in configlistnames:
            configlistname = sort.reverseconfigitemreplace(configlistname)
            temp.append(configlistname)
        configlistnames = temp
        del temp
        
    
    return newaddons, configlistnames, presetchoice, repos

def chainlist(lists):
    from itertools import chain
    lists = list(chain.from_iterable(lists))
    return lists