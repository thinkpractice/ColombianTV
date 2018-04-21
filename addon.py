# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from kodiswift import Plugin
from rcn import RcnScraper

plugin = Plugin()
rcnScraper = RcnScraper()

@plugin.route('/')
def index():
    return [channel.toItem(plugin) for channel in rcnScraper.channels]

@plugin.route("/channel/<channelUrl>/")
def show_programs(channelUrl):
    channel = rcnScraper.channelFor(channelUrl)
    return [program.toItem(plugin) for program in channel.programs]
    
@plugin.route("/program/<programUrl>")
def show_episodes(programUrl):
    program = rcnScraper.programFor(programUrl)
    return [episode.toItem(plugin) for episode in program.episodes]

if __name__ == '__main__':
    plugin.run()
