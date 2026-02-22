# Discord MusicBot with YtDL

## Pre-Requisites

- [Install ffmpeg](https://www.ffmpeg.org/), and make sure it is in PATH (make sure ffmpeg is a recognized command).
- Export your chrome cookies to a cookies.txt and place in the same folder as main.py.
- Edit [config.py](https://github.com/meowatthemoon/DiscordMusicBot_YtDl/blob/main/config.py) and place your discord token.

# (Optional) Create and activate virtual environment

```
uv venv
```

# Install Packages

```
uv pip install -r requirements.txt
uv pip install -U "yt-dlp[default]"
```

# Run

```
python3 main.py
```

- In discord run /setup_music_bot and enjoy!

# Implemented Features

- Search for songs ✓
- Play and Queue songs ✓
- Pause ✓
- Resume ✓
- Stop ✓
- Next ✓
- Previous ✓
