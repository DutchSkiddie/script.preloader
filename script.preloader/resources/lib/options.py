def GetPresetOptions():
    repolist = ['repository.jurialmunkey','repository.otaku','repository.thecrew', 'repository.ivarbrandt.test', 'repository.titan.bingie.mod', 'repository.autowidget', 'repository.nixgates', 'repository.cocoscrapers']
    addonlist = ['skin.arctic.horizon.2','script.trakt','script.embuary.info','plugin.video.themoviedb.helper','plugin.video.thecrew','plugin.video.otaku', 'service.upnext', 'skin.nimbus', 'script.nimbus.helper', 'plugin.video.seren', 'plugin.program.autowidget', 'plugin.video.fen', 'plugin.video.fenlight', 'script.module.cocoscrapers']
    
    return repolist, addonlist

def GetProviders():
    movieproviders = ['plugin.video.thecrew', 'plugin.video.seren', 'plugin.video.fen', 'plugin.video.fenlight']
    animeproviders = ['plugin.video.otaku']
    trackingproviders = ['script.trakt']
    scripts = ['script.embuary.info', 'plugin.video.themoviedb.helper', 'plugin.program.autowidget', 'script.module.cocoscrapers']
    services = ['service.upnext']
    
    return movieproviders, animeproviders, trackingproviders, scripts, services


def GetPresetDepends(addon):
    dependencies = []
    if (addon == 'skin.arctic.horizon.2'):
        dependencies.append('script.embuary.info')
        dependencies.append('plugin.video.themoviedb.helper')
    if (addon == 'skin.nimbus'):
        dependencies.append('script.nimbus.helper')
        dependencies.append('script.embuary.info')
        dependencies.append('plugin.video.themoviedb.helper')
    if (addon == 'plugin.video.fen') or (addon == 'plugin.video.fenlight'):
        dependencies.append('script.module.cocoscrapers')
    return dependencies

def GetPresetRepos(addons):
    repolist = []
    for addon in addons:
        if (addon == 'skin.arctic.horizon.2') or (addon == 'plugin.video.themoviedb.helper'):
            repolist.append('repository.jurialmunkey')
        if (addon == 'skin.nimbus'):
            repolist.append('repository.ivarbrandt.test')
        if (addon == 'plugin.video.thecrew'):
            repolist.append('repository.thecrew')
        if (addon == 'plugin.video.seren'):
            repolist.append('repository.nixgates')
        if (addon == 'plugin.video.otaku'):
            repolist.append('repository.otaku')
        if (addon == 'plugin.program.autowidget'):
            repolist.append('repository.autowidget')
        if (addon == 'plugin.video.fen') or (addon == 'plugin.video.fenlight') or (addon == 'script.module.cocoscrapers'):
            repolist.append('repository.cocoscrapers')
    
    return repolist