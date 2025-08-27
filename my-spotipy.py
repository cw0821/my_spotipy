import subprocess
import argparse
import base64

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

def rewind(seconds=10):
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

def get_album_art(output_file="album_art.jpg"):
    # AppleScript to get artwork as raw data
    script = '''
    tell application "Spotify"
        if it is running then
            set artData to artwork of current track
            set artFormat to format of artwork of current track
            set encoded to (do shell script "base64 <<<" & quoted form of (artData as «class PNGf»))
            return encoded
        else
            return "Spotify is not running."
        end if
    end tell
    '''
    encoded = run_applescript(script)
    if "Spotify is not running." in encoded:
        return encoded

    # Decode base64 to file
    with open(output_file, "wb") as f:
        f.write(base64.b64decode(encoded))
    return f"Album art saved to {output_file}"


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
        print(rewind(args.rewind))
    if args.art:
        print(get_album_art(args.art))
