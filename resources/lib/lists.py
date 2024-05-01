import os
from resources.lib import custom
from resources.lib import sort

def AddonList(zip, lastusedaddons, lastusedaddonconfigtxt, setupchoice, pathkodi):
    newaddonlist = []
    newaddonconfignames = []
    configlistnames = []
    finalList = []
    
    if(lastusedaddonconfigtxt != ''):
        lastusedaddonconfig = lastusedaddonconfigtxt.split(',')
    else:
        lastusedaddonconfig = []
    
    if (setupchoice != 2):
        from zipfile import ZipFile
        with ZipFile(zip) as compare1:
            newaddons = compare1.namelist()
    else:
        newaddons = os.listdir(pathkodi + os.sep + 'addons')       
    
    if (setupchoice != 2):
        for configitem in newaddons:
            if (configitem.startswith('addons') and (configitem.startswith('addons/packages/') == False)) and (configitem.endswith('addon.xml')):
                aoname = configitem.split('/')[1]
                newaddonconfignames.append(aoname)
                newaddonlist.append(configitem)
    else:
        for configitem in newaddons:
            if ((configitem.startswith('packages') == False)):
                newaddonconfignames.append(configitem)
                newaddonlist.append(configitem)
                  
    
    if(str(newaddons) == str(lastusedaddons)):        
        finalList, lastUsedConfig = sort.FilterAddons(newaddonconfignames, lastusedaddonconfig)   
                
    else:
        finalList, lastUsedConfig = sort.FilterAddons(newaddonconfignames, lastusedaddonconfig)         
    
    
    if (setupchoice == 0):
        configlistnames = (custom.CustomizeAddons(finalList, lastusedaddonconfig, pathkodi))
        skin = configlistnames[:1]
        configlistnames = configlistnames[1:]    
        configlistnames = chainlist(configlistnames)    
        configlistnames = chainlist(configlistnames)
        configlistnames = skin + configlistnames
    if (setupchoice == 1):
        temp = []
        configlistnames, lastused = sort.FilterAddons(newaddonconfignames, lastUsedConfig)
        for configlistname in configlistnames:
            configlistname = sort.reverseconfigitemreplace(configlistname)
            temp.append(configlistname)
        configlistnames = temp
        del temp
             
    if (setupchoice == 2):
        temp = []        
        configlistnames, lastused = sort.FilterAddons(newaddonconfignames, lastUsedConfig)
        for configlistname in configlistnames:
            configlistname = sort.reverseconfigitemreplace(configlistname)
            temp.append(configlistname)
        configlistnames = temp
        del temp
    
    return newaddons, configlistnames

def chainlist(lists):
    from itertools import chain
    lists = list(chain.from_iterable(lists))
    return lists