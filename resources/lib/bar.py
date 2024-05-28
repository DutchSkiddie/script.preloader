import sys
import os
import xbmc
import xbmcgui
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import vars

# FILENAME = ''
# DESTINATION = ''
dbxtoken = vars.getdbxtoken()

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
    global dbxtoken
    
    logged, uid, uname, umail = tokencheck()
    if not logged:
        while not logged:
            logged = dbxlogin()
        logged, uid, uname, umail = tokencheck()
        vars.setdbxtoken(dbxtoken)
        
    response = xbmcgui.Dialog().yesnocustom('[COLOR goldenrod]DROPBOX[/COLOR]', '[COLOR goldenrod][UID][/COLOR]: ' + str(uid) + '\n[COLOR goldenrod][UNAME][/COLOR]: ' + str(uname) + '\n[COLOR goldenrod][EMAIL][/COLOR]: ' + str(umail), 'CONTINUE', 'EXIT', 'LOGOUT')
    if response == -1 or response == 0:
        exit()
    elif response == 1:
        dbxtoken = ''
        vars.setdbxtoken(dbxtoken)
        init()
    elif response == 2:        
        response = xbmcgui.Dialog().yesnocustom('[COLOR goldenrod]DROPBOX SYNC[/COLOR]', '[COLOR goldenrod][UID][/COLOR]: ' + str(uid) + '\n[COLOR goldenrod][UNAME][/COLOR]: ' + str(uname) + '\n[COLOR goldenrod][EMAIL][/COLOR]: ' + str(umail), 'CONFIG', 'BACK', 'BACKUPS')
        if response == -1 or response == 0:
            init()
        elif response == 1:
            xbmcgui.Dialog().textviewer('BACKUPS', 'BACKUPS')
            response = xbmcgui.Dialog().yesnocustom('[COLOR goldenrod]DROPBOX ~BACKUPS~[/COLOR]', '[COLOR goldenrod][UID][/COLOR]: ' + str(uid) + '\n[COLOR goldenrod][UNAME][/COLOR]: ' + str(uname) + '\n[COLOR goldenrod][EMAIL][/COLOR]: ' + str(umail), 'SAVE TO DBX', 'BACK', 'LOAD FROM DBX')
            if response == -1 or response == 0:
                init()
            if response == 1:
                print('LOAD FROM DBX')
            elif response == 2:
                print('SAVE TO DBX')
        elif response == 2:
            xbmcgui.Dialog().textviewer('CONFIG', 'CONFIG')
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
                with dropbox.Dropbox(dbxtoken) as dbx:
                    try:
                        dbx.files_download_to_file(addonsxmluser, '/custom/addons.xml')
                        dbx.files_download_to_file(reposxmluser, '/custom/repos.xml')
                    except:
                        xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Something went wrong.')
            elif response == 2:
                with dropbox.Dropbox(dbxtoken) as dbx:
                    backup(dbx, addonsxml, '/custom/addons.xml')
                    backup(dbx, reposxml, '/custom/repos.xml')
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
    global dbxtoken
    
    if (len(dbxtoken) == 0):
        logged = False
        uid = ''
        uname = ''
        umail = ''
    else:
        with dropbox.Dropbox(dbxtoken) as dbx:
            try:
                account = dbx.users_get_current_account()
                uid = account.account_id.replace('dbid:', '')
                uname = account.name.display_name
                umail = account.email
                logged = True
            except AuthError:
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Invalid token.')
                dbxtoken = ''
                uid = ''
                uname = ''
                umail = ''
                logged = False
    return logged, uid, uname, umail

def dbxlogin():
    global dbxtoken
    
    reponse = xbmcgui.Dialog().yesno('[COLOR goldenrod]DROPBOX LOGIN[/COLOR]', '', 'EXIT', 'LOGIN')
    if reponse:
        keyboard = xbmc.Keyboard(dbxtoken, 'DROPBOX TOKEN')
        keyboard.doModal()
        if keyboard.isConfirmed():
            dbxtoken = keyboard.getText()
        if (len(dbxtoken) == 0):
            xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Missing token.')
            logged = False
            return logged
        with dropbox.Dropbox(dbxtoken) as dbx:
            try:
                dbx.users_get_current_account()
                logged = True
                return logged
            except AuthError:
                dbxtoken = ''
                xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Invalid token.')
                logged = False
                return logged
    else:
        exit()