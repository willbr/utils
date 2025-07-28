#!/usr/bin/env python3

import os
import subprocess
import shutil
import argparse

def convert_wav_to_ogg(directory="."):
    """
    Converts all .wav files in a specified directory to .ogg format using FFmpeg.
    After a successful conversion, the original .wav file is deleted.

    Args:
        directory (str): The path to the directory containing .wav files.
                         Defaults to the current working directory.
    """
    # --- 1. Check for FFmpeg Dependency ---
    # shutil.which() checks if an executable is in the system's PATH.
    if not shutil.which("ffmpeg"):
        print("Error: FFmpeg is not installed or not in your system's PATH.")
        print("Please install it from https://ffmpeg.org/ and try again.")
        return  # Exit the function if FFmpeg is not found

    # --- 2. Find WAV Files ---
    # Find all files ending with .wav (case-insensitive) in the directory.
    try:
        all_files = os.listdir(directory)
        wav_files = [f for f in all_files if f.lower().endswith(".wav")]
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return

    if not wav_files:
        print(f"No .wav files found in '{directory}'.")
        return

    print(f"Found {len(wav_files)} .wav file(s). Starting conversion...")

    # --- 3. Loop and Convert Each File ---
    for wav_filename in wav_files:
        # Construct the full path for the input file
        wav_file_path = os.path.join(directory, wav_filename)
        # Construct the output filename by replacing the extension
        base_name, _ = os.path.splitext(wav_filename)
        ogg_filename = f"{base_name}.ogg"
        ogg_file_path = os.path.join(directory, ogg_filename)

        # Construct the ffmpeg command as a list of arguments for security and clarity.
        # -i: input file
        # -c:a libvorbis: specify the audio codec (Ogg Vorbis)
        # -y: overwrite output file if it exists without asking
        # -loglevel error: suppresses all FFmpeg output except for fatal errors
        command = [
            "ffmpeg",
            "-i", wav_file_path,
            "-c:a", "libvorbis",
            "-y",
            "-loglevel", "error",
            ogg_file_path,
        ]

        # --- 4. Execute Command and Handle Result ---
        try:
            # Execute the command. `check=True` raises an exception for non-zero exit codes.
            # `capture_output=True` prevents FFmpeg from printing to the console.
            subprocess.run(command, check=True, capture_output=True, text=True)
            
            # If the command was successful:
            print(f"Successfully converted '{wav_filename}' to '{ogg_filename}'.")
            
            # Delete the original .wav file
            os.remove(wav_file_path)
            print(f"  -> Deleted original: '{wav_filename}'")

        except subprocess.CalledProcessError as e:
            # If the command returns a non-zero exit code (error)
            print(f"Failed to convert '{wav_filename}'.")
            # The error from FFmpeg is in stderr
            print(f"  -> FFmpeg error: {e.stderr.strip()}")
        except Exception as e:
            # Handle other potential errors (e.g., file permissions)
            print(f"An unexpected error occurred with '{wav_filename}': {e}")


    print("\nConversion process finished.")

# --- Script Execution ---
# This part allows the script to be run directly from the command line,
# handling arguments gracefully.
if __name__ == "__main__":
    # Set up the argument parser to handle command-line inputs
    parser = argparse.ArgumentParser(
        description="Convert WAV audio files to OGG format using FFmpeg."
    )
    # Add an argument for the directory. It's optional and defaults to the current directory ('.').
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="The target directory containing .wav files (defaults to the current directory).",
    )
    args = parser.parse_args()

    # Call the main function with the provided directory
    convert_wav_to_ogg(args.directory)

