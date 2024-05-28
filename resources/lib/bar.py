import sys
import os
import webbrowser
import xbmc
import xbmcgui
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import vars

# FILENAME = ''
# DESTINATION = ''
refresh_token = vars.getdbxtoken()
APP_KEY = 'njswlnwp0h03qyw'

def backup(dbx, filename, destination):
    with open(filename, 'rb') as file:
        print("Uploading " + filename + " to Dropbox as " + destination + "...")
        try:
            dbx.files_upload(file.read(), destination, mode=WriteMode('overwrite'))
        except ApiError as err:
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'ERROR: Cannot back up; insufficient space.')
                exit()
            elif err.user_message_text:
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', err.user_message_text)
                exit()
            else:
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', err)
                exit()


def change_local_file(new_content):
    print("Changing contents of " + FILENAME + " on local machine...")
    with open(FILENAME, 'wb') as f:
        f.write(new_content)

def restore(dbx, rev=None):
    xbmcgui.Dialog().notification("Restoring " + DESTINATION + " to revision " + rev + " on Dropbox...")
    dbx.files_restore(DESTINATION, rev)

    print("Downloading current " + DESTINATION + " from Dropbox, overwriting " + FILENAME + "...")
    dbx.files_download_to_file(FILENAME, DESTINATION, rev)

def select_revision(dbx):
    print("Finding available revisions on Dropbox...")
    entries = dbx.files_list_revisions(DESTINATION, limit=30).entries
    revisions = sorted(entries, key=lambda entry: entry.server_modified)

    answer = xbmcgui.Dialog().select('[COLOR firebrick]REVISION SELECT[/COLOR]', revisions)
    revision = revisions[answer]
    return revision.rev

def init():
    global refresh_token
    
    logged, uid, uname, umail = tokencheck()
    if not logged:
        while not logged:
            logged = dbxlogin()
        logged, uid, uname, umail = tokencheck()
        vars.setdbxtoken(refresh_token)
        
    response = xbmcgui.Dialog().yesnocustom('[COLOR goldenrod]DROPBOX[/COLOR]', '[COLOR goldenrod][UID][/COLOR]: ' + str(uid) + '\n[COLOR goldenrod][UNAME][/COLOR]: ' + str(uname) + '\n[COLOR goldenrod][EMAIL][/COLOR]: ' + str(umail), 'CONTINUE', 'EXIT', 'LOGOUT')
    if response == -1 or response == 0:
        exit()
    elif response == 1:
        refresh_token = ''
        vars.setdbxtoken(refresh_token)
        init()
    elif response == 2:        
        response = xbmcgui.Dialog().yesnocustom('[COLOR goldenrod]DROPBOX SYNC[/COLOR]', '[COLOR goldenrod][UID][/COLOR]: ' + str(uid) + '\n[COLOR goldenrod][UNAME][/COLOR]: ' + str(uname) + '\n[COLOR goldenrod][EMAIL][/COLOR]: ' + str(umail), 'CONFIG', 'BACK', 'BACKUPS')
        if response == -1 or response == 0:
            init()
        elif response == 1:
            response = xbmcgui.Dialog().yesnocustom('[COLOR goldenrod]DROPBOX ~BACKUPS~[/COLOR]', '[COLOR goldenrod][UID][/COLOR]: ' + str(uid) + '\n[COLOR goldenrod][UNAME][/COLOR]: ' + str(uname) + '\n[COLOR goldenrod][EMAIL][/COLOR]: ' + str(umail), 'SAVE TO DBX', 'BACK', 'LOAD FROM DBX')
            if response == -1 or response == 0:
                init()
            if response == 1:
                xbmcgui.Dialog().ok('NOT YET', 'PLEASE BE PATIENT.')
            elif response == 2:
                pathbackups = os.path.normpath(vars.PathBackups())
                backupzips = [str(os.path.relpath(os.path.join(root, file), pathbackups)).split(os.sep)[0] for root, dirs, files in os.walk(pathbackups) for file in files if '_full_' in file or '_config_' in file]
                backupzips.append('[BROWSE]')
                response = xbmcgui.Dialog().select('[COLOR firebrick]|Preloaded|[/COLOR]\t[COLOR goldenrod][BACKUP MANAGER][/COLOR]', backupzips, 0, 0, True)
                if response == -1:
                    init()
                elif backupzips[response] == '[BROWSE]':
                    browsing = True
                    while browsing == True:
                        backupzip = xbmcgui.Dialog().browse(2, '[COLOR goldenrod]FILE BROWSER[/COLOR]', '')
                        if '_full_' in backupzip or '_config_' in backupzip:
                            browsing = False
                        elif backupzip == '':
                            init()
                        else:
                            xbmcgui.Dialog().notification('[COLOR goldenrod]ERROR[/COLOR]', 'Invalid backup, check name.')
                            init()
                basename = os.path.basename(backupzip)
                with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
                    try:
                        backup(dbx, backupzip, '/backups/' + basename)
                        xbmcgui.Dialog().notification('[COLOR goldenrod]SUCCESS[/COLOR]', 'Backup saved.')
                    except:
                        xbmcgui.Dialog().notification('[COLOR goldenrod]ERROR[/COLOR]', 'Something went wrong.')
                
        elif response == 2:
            addonsxmluser = os.path.join(vars.PathAddonUserdata(), 'addons.xml')
            reposxmluser = os.path.join(vars.PathAddonUserdata(), 'repos.xml')
            
            if os.path.isfile(addonsxmluser):
                addonsxml = addonsxmluser
            else:
                addonsxml = os.path.join(vars.PathCustom(), 'addons.xml')
            if os.path.isfile(reposxmluser):
                reposxml = reposxmluser
            else:
                reposxml = os.path.join(vars.PathCustom(), 'repos.xml')
            
            response = xbmcgui.Dialog().yesnocustom('[COLOR goldenrod]DROPBOX ~CONFIG~[/COLOR]', '[COLOR goldenrod][UID][/COLOR]: ' + str(uid) + '\n[COLOR goldenrod][UNAME][/COLOR]: ' + str(uname) + '\n[COLOR goldenrod][EMAIL][/COLOR]: ' + str(umail), 'SAVE TO DBX', 'BACK', 'LOAD FROM DBX')
            if response == -1 or response == 0:
                init()
            if response == 1:
                with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
                    try:
                        dbx.files_download_to_file(addonsxmluser, '/custom/addons.xml')
                        dbx.files_download_to_file(reposxmluser, '/custom/repos.xml')
                        xbmcgui.Dialog().notification('[COLOR goldenrod]SUCCESS[/COLOR]', 'Configuration files synced.')
                    except:
                        xbmcgui.Dialog().notification('[COLOR goldenrod]ERROR[/COLOR]', 'Something went wrong.')
            elif response == 2:
                with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
                    try:
                        backup(dbx, addonsxml, '/custom/addons.xml')
                        backup(dbx, reposxml, '/custom/repos.xml')
                        xbmcgui.Dialog().notification('[COLOR goldenrod]SUCCESS[/COLOR]', 'Configuration files saved.')
                    except:
                        xbmcgui.Dialog().notification('[COLOR goldenrod]ERROR[/COLOR]', 'Something went wrong.')
                    # except:
                    #     xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Something went wrong saving addons.xml')
                    # try:
                    #     backup(dbx, reposxml, '/custom/repos.xml')
                    # except:
                    #     xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Something went wrong saving repos.xml')
                
                
    # return logged, uid, uname, umail
        # if action == 'change_local_file':
        #     change_local_file(b"updated")
        #     backup(dbx)
                
        # if action == 'select_revision':
        #     to_rev = select_revision(dbx)
        #     restore(dbx, to_rev)


def tokencheck():
    global refresh_token
    
    if (len(refresh_token) == 0):
        logged = False
        uid = ''
        uname = ''
        umail = ''
    else:
        with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
            try:
                account = dbx.users_get_current_account()
                uid = account.account_id.replace('dbid:', '')
                uname = account.name.display_name
                umail = account.email
                logged = True
            except AuthError:
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Invalid token.')
                refresh_token = ''
                uid = ''
                uname = ''
                umail = ''
                logged = False
    return logged, uid, uname, umail

def dbxlogin():
    global refresh_token
    logged = False
    dbxauthcode = ''
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')    
    reponse = xbmcgui.Dialog().yesno('[COLOR goldenrod]DROPBOX LOGIN[/COLOR]', '', 'EXIT', 'LOGIN')
    if reponse:
        webbrowser.open(auth_flow.start())
        while not logged:
            keyboard = xbmc.Keyboard(dbxauthcode, '[COLOR goldenrod]Authorization code[/COLOR]')
            keyboard.doModal()
            if keyboard.isConfirmed():
                dbxauthcode = keyboard.getText()
            if (len(dbxauthcode) == 0):
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Missing authorization code.')
                logged = False
                return logged
            try:
                oauth_result = auth_flow.finish(dbxauthcode)
                refresh_token = oauth_result.refresh_token
            except Exception as e:
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Error: ' + e)
                logged = False
                return logged
            
            with dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=APP_KEY) as dbx:
                try:
                    dbx.users_get_current_account()
                    logged = True
                    return logged
                except AuthError:
                    refresh_token = ''
                    xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Invalid token.')
                    logged = False
                    return logged
    else:
        exit()