import subprocess
import argparse

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify CLI Controller (macOS only)")
    parser.add_argument("--current", action="store_true", help="Show currently playing track")
    parser.add_argument("--play", action="store_true", help="Resume playback")
    parser.add_argument("--pause", action="store_true", help="Pause playback")
    parser.add_argument("--ff", type=int, default=0, help="Fast forward by given seconds")
    parser.add_argument("--rewind", type=int, default=0, help="Rewind by given seconds")
    
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
