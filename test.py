from providers.auto_embed1 import AutoEmbed1
from providers.auto_embed2 import AutoEmbed2
from providers.two_embed import TwoEmbed
import json
imdbID = "tt14513804"
mediaType = "movie"
title = "Captain America: Brave New World"
year = "2025"
season = None
episode = None

providers = [
    AutoEmbed1(),
    AutoEmbed2(),
    TwoEmbed(),
]

def get_streams(imdbID, mediaType, title, year, season=None, episode=None):
    video_data_list = []
    for provider in providers:
        video_data = provider.scrape(imdbID, mediaType, title, year, season, episode)
        if video_data:
            video_data_list.extend(video_data)
    return json.dumps(video_data_list, indent=4)

data = get_streams(imdbID, mediaType, title, year, season, episode)
print(data)