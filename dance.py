#!/usr/bin/python3
from gpiozero import Button
import time
import glob
import pygame
import shutil
import random
#initialization block.  Load audio player, RPI button controller on GPIO #10 and set paths for audio files
pygame.init()
button = Button(10)
song_folder = '/home/pi/5MDB/playlist/'
played_song_folder = '/home/pi/5MDB/played/'
alert = '/home/pi/5MDB/alarm.wav'

# Searches playlist directory (path) for all mp3s then populates playlist from that
def build_playlist():
    playlist = [mp3 for mp3 in glob.glob(song_folder + "*.mp3", recursive=True)]
    # If the directory is empty move played directory and rebuild
    if len(playlist) == 0:
        reset_files()
    random.shuffle(playlist)
    print(playlist)
    return playlist


# Moves files back to active directory then calls build_paylist
def reset_files():
    directory = [mp3 for mp3 in glob.glob(played_song_folder + "*.mp3", recursive=True)]
    for file in directory:
        moveback = song_folder + file.strip(played_song_folder)
        shutil.move(file, moveback)
        print('Played files moved back to main directory')
        return


# If music is playing, stop the music
def stop_music():
    pygame.mixer.music.stop()
    print("Music Stopped")
    time.sleep(1) #this prevents multiple executes on a slow button push
    return

# This plays the alert, loads the next song to play, plays the song and moves the file to the played folder.
def play_music(playlist_index):
    pygame.mixer.Sound(alert).play()
    time.sleep(8) # This let's the alert play before loading the actual song
    pygame.mixer.music.load(playlist[playlist_index])
    pygame.mixer.music.play()
    print(playlist[playlist_index].strip(song_folder), ' now playing')
    return played_song_folder + playlist[playlist_index].strip(song_folder)

def move_file(playlist_index):
    justplayed = played_song_folder + playlist[playlist_index].strip(song_folder)
    if playlist[-1] == playlist[playlist_index]:
        reset_files()
        
    
# Define our playlist variable by calling build function
playlist = build_playlist()

# Set index for playlist[i] and enter while loop to detect button press
i = 0
while True:
    # When button is pushed trigger music stop, play alert, play next song and move it to played folder
    if button.is_pressed and pygame.mixer.music.get_busy() == 0 and len(playlist) == 0:
        reset_files()
        playlist = build_playlist()
        i = 0
        play_music(i)
        move_file(i)
        i += 1
    elif button.is_pressed and pygame.mixer.music.get_busy() == 1:
        stop_music()
    elif button.is_pressed and pygame.mixer.music.get_busy() == 0:
        try:
            play_music(i)
            move_file(i)
            i += 1
            print(playlist[i].strip(song_folder), ' is up next')
        except pygame.error:
            playlist = build_playlist()
            play_music(i)
            move_file(i)
            i += 1

