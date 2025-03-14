TOKEN = 'YOUR_TOKEN_HERE'

COGS_FOLDER = "./cogs"
COMMAND_PREFIX = "!"

HISTORY_SIZE = 100
NOTIFICATION_EXPIRATION_TIME = 5
SEARCH_SONG_ITEMS_PER_PAGE = 10
NUMBER_SONGS_PER_SEARCH = 5

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -c:a libopus -b:a 96k"
}

YDL_OPTIONS = {
    "cookiefile": "cookies.txt",
    "format": "bestaudio[abr<=96]/bestaudio",
    "noplaylist": True,
    "youtube_include_dash_manifest": False,
    "youtube_include_hls_manifest": False
}
