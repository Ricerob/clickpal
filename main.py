import glob
import os
import subprocess

if __name__ == "__main__":
    # Find all MP3 files in examples directory
    tracks = glob.glob("./examples/*.mp3")
    
    if not tracks:
        print("No MP3 files found in examples directory")
        exit(1)
        
    # Create base output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Process each track
    for track in tracks:
        # Get track name without extension and path
        track_name = os.path.splitext(os.path.basename(track))[0]
        output_dir = "output"  # Just use the base output directory
        
        print(f"Processing {track}...")
        cmd = ["spleeter", "separate", "-o", output_dir, "-p", "spleeter:4stems", track]
        subprocess.run(cmd, check=True)
        print(f"Finished processing {track} -> {output_dir}")

