from resources.lib import dialog
from resources.lib import setup  


if (__name__ == '__main__'):    
    dialog.Welcome()
    setupchoice = dialog.ChooseSetup()
    setup.Setup(setupchoice)
    setup.Exit(setupchoice)