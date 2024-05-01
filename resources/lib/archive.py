import xbmcgui
import xbmcaddon
import os

def ExtractZip(notify, pathkodi, CustomZip):
    longList = []
    shortList = []
    i = 0
    o = 0
    e = 0
    from zipfile import ZipFile
    with ZipFile(CustomZip) as setup:
        for item in setup.namelist():
            if os.path.exists(pathkodi + os.sep + item) or os.path.isfile(pathkodi + os.sep + item):
                if item.startswith('addons') and notify == True:
                    longList.append('Already installed: ' + item)
                    i+=1
                else:
                    setup.extract(item, pathkodi)
                    longList.append('Overwritten: ' + item)
                    o+=1
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
    CustomZips = []
    for file in os.listdir(pathzip):
        if file.endswith(".zip"):
            from zipfile import ZipFile
            with ZipFile(pathzip + os.sep + file) as checkup:
                c=0
                zips = checkup.namelist()
                for i in zips:
                    if 'addons' in i:
                        c+=1
                if (c > 0):
                    CustomZips.append(file)    
    
    try:
        indexy = CustomZips.index(str(os.path.basename(lastused)))
        zipselect = xbmcgui.Dialog().select('Select your .zip file', CustomZips, 0, indexy, False)
        CustomZip = pathzip + CustomZips[zipselect]
    except:
        zipselect = xbmcgui.Dialog().select('Select your .zip file', CustomZips, 0, 0, False)
        CustomZip = pathzip + CustomZips[zipselect]
        
    if (zipselect == -1):
            quit()
    
    xbmcaddon.Addon().setSetting('lastused', CustomZip)
    return [CustomZip, CustomZips]


def ArchiveZip(pathaddons, pathuserdata, pathaddon, skin, pathkodi):
    import zipfile
    from datetime import datetime
    now = datetime.now()
    now = str(now).replace(' ', '_').replace(':', '.')
    filename = str(skin) + '-' + now + '.zip'
    filepath = os.path.join(pathaddon, filename)
    
    if (os.path.isdir(pathaddons) and os.path.isdir(pathuserdata)):
        c=0
        d=0
        
        with zipfile.ZipFile(filepath, 'a', zipfile.ZIP_DEFLATED) as checkup:
            xbmcgui.Dialog().notification('[COLOR firebrick]Preloader[/COLOR]', 'BACKUP STARTED', '', 10000, True)
            # checkup.open()
            for root, dirs, files in os.walk(pathkodi):
                for file in files:
                    if ('addons' in root) == True or ('userdata' in root) == True:
                        if (str(now) in str(file)) == False and (str(now) in str(root)) == False and ('custom' in root) == False and ('presets' in root) == False:
                            temp = os.path.join(root, file)
                            checkup.write(temp, os.path.relpath(temp, pathkodi))
                            c+=1
                
                for dir in dirs:
                    if ('addons' in root) == True or ('userdata' in root) == True:
                        if (str(now) in str(file)) == False and (str(now) in str(root)) == False and ('custom' in root) == False and ('presets' in root) == False:
                            if (os.path.relpath(os.path.join(root, dir)) in checkup.namelist()) == False:
                                temp = os.path.join(root, dir)
                                checkup.write(temp, os.path.relpath(temp,pathkodi))
                                d+=1
            checkup.close()           

    xbmcgui.Dialog().textviewer('SUCCESS!', str(c) + ' items succesfully archived in ' + os.path.relpath(filepath, pathkodi))
    print('PRINT: \n' + 'SUCCESS!\n' + str(c) + ' items succesfully archived\n')