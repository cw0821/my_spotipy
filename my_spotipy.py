# Filename: my-spotipy.py

import subprocess
import argparse
import base64
import requests
import os

def run_applescript(script):
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return result.stdout.strip()

def get_current_track():
    script = '''
    tell application "Spotify"
        if it is running then
            set track_name to name of current track
            set artist_name to artist of current track
            set album_name to album of current track
            return track_name & "||" & artist_name & "||" & album_name
        else
            return "Spotify is not running."
        end if
    end tell
    '''
    output = run_applescript(script)
    if "Spotify is not running." in output:
        return output
    track, artist, album = output.split("||")
    return f"Track Title: {track}\nArtist Name: {artist}\nAlbum Name: {album}"

def get_playback_state():
    script = '''
    tell application "Spotify"
        if it is running then
            set playerState to player state
            if playerState is playing then
                return "playing"
            else
                return "paused"
            end if
        else
            return "stopped"
        end if
    end tell
    '''
    return run_applescript(script)

def pause_playback():
    run_applescript('tell application "Spotify" to if it is running then pause')
    return "Playback paused."

def play_playback():
    run_applescript('tell application "Spotify" to if it is running then play')
    return "Playback started."

def fast_forward(seconds=10):
    script = f'''
    tell application "Spotify"
        if it is running then
            set currentPos to player position
            set player position to (currentPos + {seconds})
        end if
    end tell
    '''
    run_applescript(script)
    return f"Fast forwarded {seconds} seconds."

def rewind_playback(seconds=10):
    script = f'''
    tell application "Spotify"
        if it is running then
            set currentPos to player position
            if currentPos > {seconds} then
                set player position to (currentPos - {seconds})
            else
                set player position to 0
            end if
        end if
    end tell
    '''
    run_applescript(script)
    return f"Rewinded {seconds} seconds."

def save_album_art(output_file="album_art.jpg"):
    script = '''
    tell application "Spotify"
        if it is running then
            try
                set artUrl to artwork url of current track
                if artUrl is not missing value then
                    return artUrl
                else
                    return "No album art"
                end if
            on error
                return "No album art"
            end try
        else
            return "No album art"
        end if
    end tell
    '''
    art_url = run_applescript(script)
    
    if art_url == "No album art":
        if os.path.exists(output_file):
            os.remove(output_file)
        return "No album art available for this track."

    try:
        response = requests.get(art_url, timeout=5)
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            return f"Album art saved to {output_file}"
        else:
            if os.path.exists(output_file):
                os.remove(output_file)
            return f"Failed to download album art. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        if os.path.exists(output_file):
            os.remove(output_file)
        return f"An error occurred: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify CLI Controller (macOS only)")
    parser.add_argument("--current", action="store_true", help="Show currently playing track")
    parser.add_argument("--play", action="store_true", help="Resume playback")
    parser.add_argument("--pause", action="store_true", help="Pause playback")
    parser.add_argument("--ff", type=int, default=0, help="Fast forward by given seconds")
    parser.add_argument("--rewind", type=int, default=0, help="Rewind by given seconds")
    parser.add_argument("--art", type=str, nargs="?", const="album_art.jpg", help="Save current album art to file (default: album_art.jpg)")
    
    args = parser.parse_args()

    if args.current:
        print(get_current_track())
    if args.play:
        print(play_playback())
    if args.pause:
        print(pause_playback())
    if args.ff > 0:
        print(fast_forward(args.ff))
    if args.rewind > 0:
        print(rewind_playback(args.rewind))
    if args.art:
        print(save_album_art(args.art))