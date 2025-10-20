# Clickpal

Automates:
1. Split tracks into stems with [Spleeter](https://github.com/deezer/spleeter).  
2. Import stems into [Audacity](https://www.audacityteam.org/) via scripting.  
3. Export a combined track.

---

## Setup

```bash
# Create environment
conda create -n spleeter-env python=3.9 --no-default-packages
conda activate spleeter-env

# Install deps
conda install -c conda-forge ffmpeg tensorflow=2.9 numba
pip install -r requirements.txt
```

## Prerequisites

**⚠️ IMPORTANT: Audacity must be running with scripting enabled before running the script.**

1. **Open Audacity** and enable scripting:
   - Go to `Tools` → `Scriptables` → `New` (or `Edit` → `Preferences` → `Modules`)
   - Enable "Scriptables" module
   - Restart Audacity if prompted

2. **Keep Audacity open** while running the script - it needs to be running to receive commands.

## Usage

### Method 1: Local Files

Place your MP3 files in the `examples/` directory and run:

! There's a glitch with having multiple files. Just use with one for now. Audacity piping is failing to clear tracks before importing

```bash
python main.py
```

This will:
1. Process all MP3 files in the `examples/` directory using Spleeter's 4-stem separation
2. Import the separated stems (bass, drums, other, vocals) into Audacity
3. Export a combined mixdown to `output/combined/[track_name].mp3`

### Method 2: YouTube Videos

Download and process YouTube videos directly:

```bash
python main.py --link "https://www.youtube.com/watch?v=VIDEO_ID"
```

This will:
1. Download the video from YouTube
2. Extract audio and convert to MP3
3. Process with Spleeter (4-stem separation)
4. Import stems into Audacity
5. Export combined mixdown
6. Clean up temporary files automatically

### Command Line Options

#### `--link URL`
Download and process a YouTube video instead of using local files:

```bash
python main.py --link "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### `--nodrums`
Skip importing the drums stem into Audacity:

```bash
python main.py --nodrums
python main.py --link "https://youtube.com/watch?v=VIDEO_ID" --nodrums
```

#### `--export PATH`
Specify a custom export path for the final mixdown:

```bash
python main.py --export /path/to/custom/output.mp3
python main.py --link "https://youtube.com/watch?v=VIDEO_ID" --export ./my_mix.mp3
```

#### `--save-project PATH`
Save the Audacity project file (.aup3) after processing:

```bash
python main.py --save-project /path/to/project.aup3
python main.py --link "https://youtube.com/watch?v=VIDEO_ID" --save-project ./my_project.aup3
```

### Combined Options

You can combine multiple options:

```bash
# Local file with custom export and project save
python main.py --nodrums --export ./my_mix.mp3 --save-project ./my_project.aup3

# YouTube video with custom export (no drums)
python main.py --link "https://youtube.com/watch?v=VIDEO_ID" --nodrums --export ./youtube_mix.mp3
```

## Requirements

- **Audacity** must be running with scripting enabled (see Prerequisites above)
- **Spleeter** with 4-stem model (automatically downloaded on first use)
- **yt-dlp** for YouTube downloads (automatically installed)
- For local processing: MP3 files in the `examples/` directory
- For YouTube processing: Valid YouTube URL

## Output Structure

```
output/
├── [track_name]/
│   ├── bass.wav
│   ├── drums.wav
│   ├── other.wav
│   └── vocals.wav
└── combined/
    └── [track_name].mp3
```

## Audacity Integration

The script communicates with Audacity through named pipes:
- Commands are sent to `/tmp/audacity_script_pipe.to.[user_id]`
- Responses are read from `/tmp/audacity_script_pipe.from.[user_id]`

**Make sure Audacity is running and has scripting enabled before running the script.**

## Troubleshooting

### YouTube Download Issues
- Some videos may have download restrictions
- Try different YouTube URLs if one fails
- The script will automatically clean up failed downloads

### Audacity Connection Issues
- Ensure Audacity is running with scripting enabled
- Check that no other scripts are using the same pipes
- Restart Audacity if commands aren't being received

### Multiple Files
⚠️ There's a known issue with processing multiple files - the script may not clear tracks properly between imports. For best results, process one file at a time.