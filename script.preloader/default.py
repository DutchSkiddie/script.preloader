from resources.lib import dialog
from resources.lib import setup  


if (__name__ == '__main__'):    
    setupchoice = dialog.Welcome()
    setup.Setup(setupchoice)
    exit()