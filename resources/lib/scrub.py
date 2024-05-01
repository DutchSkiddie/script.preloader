import os
import xbmcgui

def ClearApis(pathkodi):
    search = ["api_key", "apikey", "token", "refresh", "user", "auth", "login", "authvar", "password"]
    pathuserdata = os.path.join(pathkodi, 'userdata', 'addon_data')

    for folder, dirs, files in os.walk(pathuserdata):
        for file in files:
            if str(file).startswith('settings') == True and str(file).endswith('.xml') == True and ('skin.' in str(folder)) == False:
                fullpath = os.path.join(folder, file)
                with open(fullpath, 'r') as fin:
                    api = 0
                    with open(fullpath + '.temp', 'a') as fout:
                        for line in fin:
                            for searched in search:
                                if searched in line:
                                    mark = line.split('>')[1]
                                    mark = mark.split('<')[0]
                                    fout.write(line.replace(mark, ''))
                                    api = api+1
                                else:
                                    fout.write(line)
                        if(api != 0):
                            xbmcgui.Dialog().textviewer('API SCRUB: ' + file, folder.replace(pathuserdata + os.sep, '') + ' has been scrubbed for Api keys.')
                                
                    fout.close()
                fin.close()
                os.remove(fullpath)
                os.rename(fullpath + '.temp', fullpath)