import sys
import dropbox
import xbmcgui
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from resources.lib import vars

TOKEN = ''
FILENAME = ''
DESTINATION = ''

def backup(dbx):
    with open(FILENAME, 'rb') as file:
        print("Uploading " + FILENAME + " to Dropbox as " + DESTINATION + "...")
        try:
            dbx.files_upload(file.read(), DESTINATION, mode=WriteMode('overwrite'))
        except ApiError as err:
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


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

def init(action):
    if (len(TOKEN) == 0):
        xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Missing token.')
        exit()
    with dropbox.Dropbox(TOKEN) as dbx:
        try:
            dbx.users_get_current_account()
        except AuthError:
            xbmcgui.Dialog().ok('[COLOR goldenrod]ERROR[/COLOR]', 'Invalid token.')
            exit()

        if action == 'change_local_file':
            change_local_file(b"updated")
            backup(dbx)
            
        if action == 'select_revision':
            to_rev = select_revision(dbx)
            restore(dbx, to_rev)


