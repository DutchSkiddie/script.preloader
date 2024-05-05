def GetPresetOptions():
    repolist = ['repository.jurialmunkey','repository.otaku','repository.thecrew']
    addonlist = ['skin.arctic.horizon.2','script.trakt','script.embuary.info','plugin.video.themoviedb.helper','plugin.video.thecrew','plugin.video.otaku', 'service.upnext']
    
    return repolist, addonlist

def GetProviders():
    movieproviders = ['plugin.video.thecrew']
    animeproviders = ['plugin.video.otaku']
    trackingproviders = ['script.trakt']
    scripts = ['script.embuary.info', 'plugin.video.themoviedb.helper']
    services = ['service.upnext']
    
    return movieproviders, animeproviders, trackingproviders, scripts, services


def GetPresetDepends(skin):
    if (skin == 'skin.arctic.horizon.2'):
        dependencies = ['script.embuary.info', 'plugin.video.themoviedb.helper']
    return dependencies

def GetPresetRepos(addons):
    repolist = []
    for addon in addons:
        if (addon == 'skin.arctic.horizon.2'):
            repolist.append('repository.jurialmunkey')
        if (addon == 'plugin.video.themoviedb.helper'):
            repolist.append('repository.jurialmunkey')
        if (addon == 'plugin.video.thecrew'):
            repolist.append('repository.thecrew')
        if (addon == 'plugin.video.otaku'):
            repolist.append('repository.otaku')
    
    return repolist