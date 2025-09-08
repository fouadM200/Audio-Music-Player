# Simple Audio and Music Player using Pygame and Tkinter
# This program allows you to select audio and video files from your computer and play them.
# You can play, pause, stop, rewind, and fast forward the media.
# You can also create a playlist by adding multiple files, removing files, and clearing the entire playlist.    

# Now you can increase or decrease the volume here, you can also select multiple songs at once and listen to your favorite songs, delete and add songs as needed.
# Remember only this files *.mp3;*.wav;*.ogg;*.mp4;*.avi;*.mkv;*.flv;*.mov;*.wmv;*.webm

import os                                      # For file path operations
import pygame                                  # For audio and video playback
from tkinter import Tk, filedialog, messagebox # For GUI and file dialog
from tkinter import ttk                        # For themed widgets
from tkinter import Listbox                    # For playlist display
import requests                                # For making HTTP requests (if needed)

# Initialize the mixer
pygame.mixer.init()

# Create a Tkinter window to select media files
root = Tk()
root.withdraw() # Hide the root window

# Global variables
current_file = ""
playlist = []
current_index = 0
is_playing = False
volume = 0.5  # Default volume

# Define all functions needed for our widgets
# 1. Function to select a file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[
        ("MP3 files", "*.mp3"),
        ("WAV files", "*.wav"),
        ("OGG files", "*.ogg"),
        ("MP4 files", "*.mp4"),
        ("AVI files", "*.avi"),
        ("MKV files", "*.mkv"),
        ("FLV files", "*.flv"),
        ("MOV files", "*.mov"),
        ("WMV files", "*.wmv"),
        ("WEBM files", "*.webm"),
        ("All files", "*.*")
    ]) # Only those file types are supported
    if file_path:
        add_to_playlist(file_path)

# 2. Function to add a file to the playlist
def add_to_playlist(file_path):
    playlist.append(file_path)
    playlist_box.insert("end", os.path.basename(file_path))

# 3. Function to remove a file from the playlist
def remove_from_playlist():
    global current_file, current_index, is_playing

    selected_index = playlist_box.curselection()
    if selected_index:
        index = selected_index[0]
        removed_file = playlist[index]

        # Check if the removed song is currently playing
        if removed_file == current_file:
            # Temporarily stop playback
            pygame.mixer.music.stop()

            # Remove the file first
            playlist.pop(index)
            playlist_box.delete(index)

            # Check if there's a next song to play
            if index < len(playlist):  # still a next song at the same index
                current_index = index
                play_music(playlist[current_index])
            else:
                # No next song; clear current state
                current_file = ""
                is_playing = False
                update_status()

        else:
            # If it's not the current song, just remove it
            playlist.pop(index)
            playlist_box.delete(index)


# 4. Function to clear the playlist
def clear_playlist():
    global current_index, current_file, is_playing
    playlist.clear()
    playlist_box.delete(0, "end")
    pygame.mixer.music.stop()
    current_file = ""
    is_playing = False
    update_status()

    # Hide Previous and Next buttons again
    previous_button.grid_remove()
    next_button.grid_remove()

# 5. Function to play the selected file or playlist
def play_music(file_path=None):
    global current_file, current_index, is_playing

    if not file_path:
        selected_index = playlist_box.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a song from the playlist before pressing Play.")
            return
        current_index = selected_index[0]
        file_path = playlist[current_index]

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    current_file = file_path
    is_playing = True

    # Unhide navigation buttons after first play
    previous_button.grid()
    next_button.grid()

    update_status()

# 6. Function to pause/resume the music
def pause_resume_music():
    global is_playing, current_file

    if not current_file:
        selected_index = playlist_box.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a song from the playlist before pressing Play.")
            return
        else:
            play_music()
            return

    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
    else:
        pygame.mixer.music.unpause()
        is_playing = True

    update_status()

# 7. Function to pause the music (no toggle)
def pause_music():
    global is_playing
    pygame.mixer.music.pause()
    is_playing = False
    update_status()

# 8. Function to play next track in the playlist
def next_track():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_music(playlist[current_index])
        update_status()

# 9. Function to play previous track in the playlist
def previous_track():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_music(playlist[current_index])
        update_status()

# 10. Function to set the volume
def set_volume(volume_level):
    global volume
    volume = float(volume_level)
    pygame.mixer.music.set_volume(volume)

# 11. Function to update the status label
def update_status():
    global current_file, current_index, is_playing

    if current_file:
        status_label.config(text=f"Now playing: {os.path.basename(current_file)}")
    else:
        status_label.config(text="")

    if is_playing:
        play_pause_button.config(text="Pause")
    else:
        play_pause_button.config(text="Play")

    playlist_box.selection_clear(0, "end")
    if playlist:
        playlist_box.selection_set(current_index)

# 12. Function to identify song info using Audd.io
def get_info_using_AI():
    global current_file

    if not current_file:
        messagebox.showerror("Error", "No song is currently playing.")
        return

    # You must replace this with your actual Audd.io API key
    api_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # Prepare the request
    try:
        with open(current_file, 'rb') as f:
            files = {
                'file': f,
            }
            data = {
                'api_token': api_token,
                'return': 'apple_music,spotify',
            }
            response = requests.post('https://api.audd.io/', data=data, files=files)

        result = response.json()

        if result['status'] == 'success' and result['result']:
            track = result['result']
            info = f"Title: {track.get('title', 'Unknown')}\n" \
                   f"Artist: {track.get('artist', 'Unknown')}\n" \
                   f"Album: {track.get('album', 'Unknown')}\n" \
                   f"Release Date: {track.get('release_date', 'Unknown')}\n"

            messagebox.showinfo("AI Music Info", info)
        else:
            messagebox.showinfo("AI Music Info", "Sorry, the song could not be identified.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")


# Main GUI window
window = Tk()
window.title("Media Player")

# Create buttons
select_button = ttk.Button(window, text="Select File", command=select_file)
previous_button = ttk.Button(window, text="<< Previous", command=previous_track)
play_pause_button = ttk.Button(window, text="Play ", command=pause_resume_music)
pause_button = ttk.Button(window, text="Pause", command=pause_music)
next_button = ttk.Button(window, text="Next >>", command=next_track)

# Create playlist controls
playlist_label = ttk.Label(window, text="Playlist")
playlist_box = Listbox(window, selectbackground="#3498db", selectforeground="white")
remove_button = ttk.Button(window, text="Remove", command=remove_from_playlist)
clear_button = ttk.Button(window, text="Clear", command=clear_playlist)
ask_AI_button = ttk.Button(window, text="Get Info using AI", command=get_info_using_AI)

# Create volume control
volume_label = ttk.Label(window, text="Volume")
volume_scale = ttk.Scale(window, from_=0.0, to=1.0, orient="horizontal", command=set_volume)
volume_scale.set(volume)  # Set initial volume value

# Create status label
status_label = ttk.Label(window, text="", anchor="center")

# Position the buttons and widgets
select_button.grid(row=0, column=0, padx=10, pady=10)
previous_button.grid(row=0, column=1, padx=10, pady=10)
play_pause_button.grid(row=0, column=2, padx=10, pady=10)
next_button.grid(row=0, column=3, padx=10, pady=10)
playlist_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
playlist_box.grid(row=2, column=0, rowspan=4, columnspan=5, padx=10, pady=10, sticky="nsew")
remove_button.grid(row=2, column=5, padx=5, pady=10, sticky="w")
clear_button.grid(row=3, column=5, padx=5, pady=10, sticky="w")
ask_AI_button.grid(row=4, column=5, padx=5, pady=10, sticky="w")
volume_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
volume_scale.grid(row=6, column=1, columnspan=4, padx=10, pady=5, sticky="we")
status_label.grid(row=7, column=0, columnspan=6, padx=10, pady=5, sticky="we")

# Configure grid weights
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)

# Hide Previous and Next buttons at startup
previous_button.grid_remove()
next_button.grid_remove()

# Start the GUI event loop
window.mainloop()

# Quit the mixer
pygame.mixer.quit()
