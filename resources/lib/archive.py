import xbmcgui
import xbmcaddon
import os
import io

def ExtractZip(notify, pathkodi, zip, preset):
    longList = []
    shortList = []
    i = 0
    o = 0
    e = 0
    
    from zipfile import ZipFile
    with ZipFile(zip) as setup:
        
        if (preset.__class__ == list):
            if (zip.endswith('optionals.zip')):
                for item in setup.namelist():
                    for p in preset:
                        if p in item:
                            if os.path.exists(os.path.join(pathkodi, item)) or os.path.isfile(os.path.join(pathkodi, item)):
                                try:
                                    if (os.path.isdir(os.path.join(pathkodi, item)) == False):
                                        os.remove(os.path.join(pathkodi, item))
                                        setup.extract(item, pathkodi)
                                        longList.append('Overwritten: ' + item)
                                    o+=1
                                except:
                                    longList.append(item + ' is being used by another process (Kodi)')
                            else:
                                setup.extract(item, pathkodi)
                                longList.append('Extracted: ' + item)
                                e+=1
                
            else:
                for item in setup.namelist():
                    for p in preset:
                        if p in item:
                            if os.path.exists(os.path.join(pathkodi, item)) or os.path.isfile(os.path.join(pathkodi, item)):
                                if item.startswith('addons'):
                                    if (notify == True):
                                        longList.append('Already installed: ' + item)
                                        i+=1
                                else:
                                    try:
                                        if (os.path.isdir(os.path.join(pathkodi, item)) == False):
                                            os.remove(os.path.join(pathkodi, item))
                                            setup.extract(item, pathkodi)
                                            longList.append('Overwritten: ' + item)
                                            o+=1
                                    except:
                                        longList.append(item + ' is being used by another process (Kodi)')
                                        
                            else:
                                setup.extract(item, pathkodi)
                                longList.append('Extracted: ' + item)
                                e+=1
        else:
            if (preset != False):
                for item in setup.namelist():
                    if item.startswith(preset) == True and ('config.txt' in item) == False:
                        item2 = item.replace(preset, '')
                        
                        if os.path.exists(os.path.join(pathkodi, item2)) or os.path.isfile(os.path.join(pathkodi, item2)):
                                setup.getinfo(item).filename = item2
                                setup.extract(item, pathkodi)
                                longList.append('Overwritten: ' + item)
                                o+=1
                        else:
                                setup.getinfo(item).filename = item2
                                setup.extract(item, pathkodi)
                                longList.append('Extracted: ' + item)
                                e+=1
                        

                
                
        if (preset == False):
            for item in setup.namelist():
                if os.path.exists(os.path.join(pathkodi, item)) or os.path.isfile(os.path.join(pathkodi, item)):
                    if item.startswith('addons'):
                        if (notify == True):
                            longList.append('Already installed: ' + item)
                            i+=1
                    else:
                        try:
                            if (os.path.isdir(os.path.join(pathkodi, item)) == False):
                                os.remove(os.path.join(pathkodi, item))
                                setup.extract(item, pathkodi)
                                longList.append('Overwritten: ' + item)
                                o+=1
                        except:
                            longList.append(item + ' is being used by another process (Kodi)')
                                
                else:
                    setup.extract(item, pathkodi)
                    longList.append('Extracted: ' + item)
                    e+=1
                    
    print('Setup succesful.\n' + str(i) + ' items already installed.\n')
    print('Setup succesful.\n' + str(o) + ' items overwritten.\n')
    print('Setup succesful.\n' + str(e) + ' new items extracted.\n')
    
    if (notify == True):
        xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', str(i) + ' items already installed.', '', 2000, True)
        xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', str(o) + ' items overwritten.', '', 2000, True)
        xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', str(e) + ' new items extracted.', '', 2000, True)
        
    for unzipFile in longList:
        unzipFile = str(unzipFile.split('/')[:2])
        if (unzipFile not in shortList):
            shortList.append(unzipFile)
        
    sshortlist = str(shortList)
    sshortlist = sshortlist.replace("']", '').replace('", "', '').replace("['", '\n').replace("', '", '/').replace('["', '').replace('"]', '')
    
    print('Details: \n' + str(sshortlist))
    if (notify == True):
        xbmcgui.Dialog().textviewer('[COLOR firebrick]~' + '{' + 'SETUP' + '}' + '~[/COLOR]', str(sshortlist))


def SelectZip(lastused, pathzip):
    ziplist = []
    configlist = []
    for file in os.listdir(pathzip):
        if file.endswith(".zip"):
            from zipfile import ZipFile
            with ZipFile(os.path.join(pathzip, file)) as checkup:
                c=0
                d=0
                conf=0
                zips = checkup.namelist()
                for i in zips:
                    if 'addons' in i:
                        c+=1
                    if 'userdata' in i:
                        d+=1
                    if 'config.txt' in i:
                        conf+=1
                if (c > 0) and (d > 0):
                    ziplist.append(file)
                    if (conf > 0):
                        configlist.append(file)    
    
    try:
        indexy = zips.index(str(os.path.basename(lastused)))
        zipselect = xbmcgui.Dialog().select('Select your .zip file', ziplist, 0, indexy, False)
        zip = os.path.join(pathzip, ziplist[zipselect])
    except:
        zipselect = xbmcgui.Dialog().select('Select your .zip file', ziplist, 0, 0, False)
        zip = os.path.join(pathzip, ziplist[zipselect])
        

    if (ziplist[zipselect] in configlist):
        with ZipFile(zip) as checkup:
            with io.TextIOWrapper(checkup.open('config.txt'), encoding="utf-8") as file:
                config = file.read()
                config = config.replace("['", '')
                config = config.replace("']", '')
                config = config.replace("', '", ',')
                config = config.split(',')
            checkup.close()
    else:
        config = False  
    
    if (zipselect == -1):
            quit()
    
    xbmcaddon.Addon().setSetting('lastused', zip)
    return [zip, config]


def ArchiveZip(pathaddons, pathuserdata, skin, pathkodi, savetype, addonconfig, repos):
    import zipfile
    from datetime import datetime
    now = datetime.now()
    now = str(now).replace(' ', '_').replace(':', '.')
    filename = str(skin) + '-' + now + '.zip'
    if (savetype == True):
        filename = 'full-' + filename
    if (savetype == False):
        filename = 'config-' + filename
        
    filepath = os.path.join(pathuserdata, 'addon_data', 'script.preloader', filename)
    
    if (os.path.isdir(pathaddons) and os.path.isdir(pathuserdata)):
        c=0
        if (savetype == True):
            with zipfile.ZipFile(filepath, 'a', zipfile.ZIP_DEFLATED) as checkup:
                xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', 'BACKUP STARTED', '', 10000, True)
                for root, dirs, files in os.walk(pathkodi):
                    for file in files:
                        if ('addons' in root) == True or ('userdata' in root) == True:
                            if ('script.preloader' in root) == False:
                                temp = os.path.join(root, file)
                                checkup.write(temp, os.path.relpath(temp, pathkodi))
                                c+=1
                checkup.close()           

        if (savetype == False):
            with zipfile.ZipFile(filepath, 'a', zipfile.ZIP_DEFLATED) as checkup:
                xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', 'BACKUP STARTED', '', 10000, True)
                for root, dirs, files in os.walk(pathkodi):
                    for file in files:
                        if ('addons' in root) == True and ('repository' in root) == True:
                            for repo in repos:
                                if (repo in root) == True:
                                    temp = os.path.join(root, file)
                                    checkup.write(temp, os.path.relpath(temp, pathkodi))
                                    c+=1
                        if ('userdata' in root) == True and ('script.preloader' in root) == False:
                            temp = os.path.join(root, file)
                            checkup.write(temp, os.path.relpath(temp, pathkodi))
                            c+=1
                checkup.writestr('config.txt', str(addonconfig))
                c+=1
                checkup.close()
                            
        
    xbmcgui.Dialog().textviewer('SUCCESS!', str(c) + ' items succesfully archived in ' + os.path.relpath(filepath, pathkodi))
    print('PRINT: \n' + 'SUCCESS!\n' + str(c) + ' items succesfully archived\n')
    
def FindPresets(skinpath):
    presets = []
    import zipfile
    with zipfile.ZipFile(skinpath, 'r', zipfile.ZIP_DEFLATED) as checkup:
        folders = checkup.namelist()
        for folder in folders:
            folder = folder.split('/')[0]
            presets.append(folder)
    presets = list(set(presets))
    return presets