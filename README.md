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

## Usage

### Basic Usage

Place your MP3 files in the `examples/` directory and run:

```bash
python main.py
```

This will:
1. Process all MP3 files in the `examples/` directory using Spleeter's 4-stem separation
2. Import the separated stems (bass, drums, other, vocals) into Audacity
3. Export a combined mixdown to `output/combined/[track_name].mp3`

### Command Line Options

#### `--nodrums`
Skip importing the drums stem into Audacity:

```bash
python main.py --nodrums
```

#### `--export PATH`
Specify a custom export path for the final mixdown:

```bash
python main.py --export /path/to/custom/output.mp3
```

#### `--save-project PATH`
Save the Audacity project file (.aup3) after processing:

```bash
python main.py --save-project /path/to/project.aup3
```

### Combined Options

You can combine multiple options:

```bash
python main.py --nodrums --export ./my_mix.mp3 --save-project ./my_project.aup3
```

## Requirements

- **Audacity** must be running with scripting enabled
- **Spleeter** with 4-stem model (automatically downloaded on first use)
- MP3 files placed in the `examples/` directory

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

Make sure Audacity is running and has scripting enabled before running the script.
