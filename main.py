import glob
import os
import subprocess
import time
import argparse

# === Audacity scripting setup ===
AUDACITY_PIPE_TO = f"/tmp/audacity_script_pipe.to.{os.getuid()}"
AUDACITY_PIPE_FROM = f"/tmp/audacity_script_pipe.from.{os.getuid()}"

def send_command(cmd: str):
    """Send a command to Audacity via pipe"""
    with open(AUDACITY_PIPE_TO, 'w') as to_aud:
        to_aud.write(cmd + '\n')
        to_aud.flush()

def get_response():
    """Read a response from Audacity"""
    with open(AUDACITY_PIPE_FROM, 'r') as from_aud:
        return from_aud.readline().strip()

# === Main ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and import tracks into Audacity")
    parser.add_argument("--nodrums", action="store_true", help="Skip importing drums stem")
    parser.add_argument("--export", type=str, help="Path to export final mix (overrides default)")
    parser.add_argument("--save-project", type=str, help="Path to save Audacity project (.aup3)")
    args = parser.parse_args()

    tracks = glob.glob("./examples/*.mp3")
    if not tracks:
        print("No MP3 files found in examples directory")
        exit(1)

    os.makedirs("output", exist_ok=True)
    os.makedirs("output/combined", exist_ok=True)

    for track in tracks:
        track_name = os.path.splitext(os.path.basename(track))[0]
        output_dir = "output"

        print(f"Processing {track} with Spleeter...")
        cmd = ["spleeter", "separate", "-o", output_dir, "-p", "spleeter:4stems", track]
        subprocess.run(cmd, check=True)
        print(f"Finished Spleeter processing -> {output_dir}")

        # Import separated stems into Audacity
        stem_dir = os.path.join(output_dir, track_name)
        if not os.path.isdir(stem_dir):
            print(f"No stems directory found for {track_name}, skipping Audacity import.")
            continue

        stems = glob.glob(os.path.join(stem_dir, "*.wav"))
        if not stems:
            print(f"No stems found for {track_name}, skipping Audacity import.")
            continue

        for stem in stems:
            stem_name = os.path.splitext(os.path.basename(stem))[0].lower()
            if args.nodrums and "drums" in stem_name:
                print(f"Skipping drums stem: {stem}")
                continue

            print(f"Importing {stem} into Audacity...")
            send_command(f'Import2: Filename="{os.path.abspath(stem)}"')
            time.sleep(0.2)
            print("Audacity response:", get_response())

        print(f"All stems from {track_name} imported into Audacity ✅")

        # Decide export path
        if args.export:
            export_path = os.path.abspath(args.export)
        else:
            export_path = os.path.abspath(f"output/combined/{track_name}.mp3")

        print(f"Exporting mixdown to {export_path}...")

        # Always select all tracks first
        send_command("SelectAll:")
        time.sleep(0.2)
        print("Audacity response:", get_response())

        # Export full mix (default stereo)
        send_command(f'Export2: Filename="{export_path}" NumChannels=2')
        time.sleep(1)
        print("Audacity response:", get_response())

        # Save project if requested
        if args.save_project:
            project_path = os.path.abspath(args.save_project)
            print(f"Saving Audacity project to {project_path}...")
            send_command(f'SaveProject2: Filename="{project_path}"')
            time.sleep(1)
            print("Audacity response:", get_response())
