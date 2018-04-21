# -*- coding: utf-8 -*-
from kodiswift import Plugin
from rcn import RcnScraper

plugin = Plugin()
rcnScraper = RcnScraper()

@plugin.route('/')
def index():
    return [channel.toItem(plugin) for channel in rcnScraper.channels]

@plugin.route("channel/<channelName>/")
def show_programs(channelName):
    channel = rcnScraper.channelFor(channelName)
    return [program.toItem(plugin) for program in channel.programs]
    
@plugin.route("program/<programName>")
def show_episodes(programName):
    program = rcnScraper.programFor(programName)
    return [episode.toItem(plugin) for episode in program.episodes]

if __name__ == '__main__':
    plugin.run()
