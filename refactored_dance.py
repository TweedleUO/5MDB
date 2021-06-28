#!/usr/bin/python3
import glob
import pygame
import random
import shutil
from os import path
from time import sleep
from gpiozero import Button

pygame.mixer.init()
button = Button(10)
alert = '/home/pi/code/5MDB/alarm.wav'
hal9000 = '/home/pi/code/5MDB/icant.wav'
song_folder = '/home/pi/code/5MDB/playlist/'
played_folder = '/home/pi/code/5MDB/played/'
media_status = None
# i is used as our global index value for iterating through our playlist object
i = 0


# Function creates a new playlist object from a location it is passed, defaults to local storage location
# We use glob to identify .mp3 files in specified location and store filenemes in a list
# Randomize the list so iteration isn't predictable
def build_playlist(upcoming='/home/pi/code/5MDB/playlist/'):
    pl = [mp3 for mp3 in glob.glob(upcoming + "*.mp3", recursive=True)]
    random.shuffle(pl)
    return pl


# Function scans default RPI mount points, and default usbmount (debian pkg)
# It searches to find a 5MDB folder with a playlist folder and played folder
# If those folders are found, we assume you have a new USB stick with music loaded for the program
def check_removable_media():
    check1 = glob.glob('/media/*/*/5MDB/playlist/')
    check2 = glob.glob('/media/*/5MDB/playlist/')
    check3 = glob.glob('/media/*/*/5MDB/played/')
    check4 = glob.glob('/media/*/5MDB/played/')
    if (len(check1) > 0 and len(check2) > 0) or (len(check3) > 0 and len(check4) > 0):
        return True
    return False


# This function updates our global path variables for file locations
# This is called when there is a change detected by our location handler
def store_path():
    global song_folder
    global played_folder
    # validator variable meant for console feedback when new path is stored
    validator = song_folder
    if check_removable_media():
        # glob returns a list as its possible there are multiple drives detected.
        s_folder = glob.glob('/media/*/*/5MDB/playlist/')
        # We run the check in the first mount location by usbmount.  This is where it is mounted if rpi is in console mode.
        if len(s_folder) > 0:
            p_folder = glob.glob('/media/*/*/5MDB/played/')
        # If nothing is detected in usbmount location (/media/usb[0-7]/...), run the check on default mount location in LXDE
        else:
            s_folder = glob.glob('/media/*/5MDB/playlist/')
            p_folder = glob.glob('/media/*/5MDB/played/')
        # we are only concerned with handling the first drive in the event multiples are detected
        played_folder = p_folder[0]
        song_folder = s_folder[0]
    # No usb drive locations detected, revert to local storage location
    else:
        song_folder = '/home/pi/code/5MDB/playlist/'
        played_folder = '/home/pi/code/5MDB/played/'
    if validator == song_folder:
        print('No Change', song_folder)
        return
    else:
        print('Updated', song_folder)
        return


# This function controls when to update our file paths
# It ensures we have a playlist being generated from the appropriate datastore
def location_handler():
    global song_folder
    global i
    global playlist
    # This condition is tiggered when we are on local storage and a usb storage location is detected
    if check_removable_media() and song_folder == '/home/pi/code/5MDB/playlist/':
        print('new media detected, updating')
        store_path()
        playlist = build_playlist(song_folder)
        # We have a new playlist generated from a new path.  reset our global index
        i = 0
        # This is a validation check that we did not create an empty playlist.
        if len(playlist) - i == 0:
            # if we did, try to locate song files in the '.../played/' folder and rebuild
            reset_played_dir()
            playlist = build_playlist(song_folder)
        print('now reading from external drive')
        return
    # If usb drive is removed, revert back to local storage.
    elif not check_removable_media() and song_folder != '/home/pi/code/5MDB/playlist/':
        print('media removed, updating')
        store_path()
        playlist = build_playlist(song_folder)
        i = 0
        if len(playlist) - i == 0:
            reset_played_dir()
            playlist = build_playlist(song_folder)
        print('now reading from local drive')
        return
    # Console feedback for current media source
    if song_folder != '/home/pi/code/5MDB/playlist/':
        print('media source USB')
    else:
        print('media source local')
    return


# This function loads and plays the current song in the playlist and moves file to played folder.
# File handling ensures we do not replay songs until all songs have been exhausted.
def load_play():
    global i
    global playlist
    global played_folder
    print('Now playing:', what_song(i))
    try:
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        shutil.move(playlist[i], played_folder)
        print('moved file to played folder')
        return
    # If our index counter ever exceeds our playlist, reset directories, index and playlist
    except IndexError:
        reset_played_dir()
        location_handler()
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        shutil.move(playlist[i], played_folder)
    # This exception can occur when a fie cannot be loaded.
    # This can be a product of our file handling or a corrupted or otherwise unplayable file.
    except pygame.error:
        reset_played_dir()
        location_handler()
        load_play()


# Return what song is at a given index point
def what_song(index):
    global playlist
    global played_folder
    this_song = playlist[index]
    return path.basename(this_song.strip('.mp3'))


# Brings all songs that have already been played, back into active playlist
# Move all songs in '.../played/' to '.../playlist'
def reset_played_dir():
    global song_folder
    global played_folder
    directory = [mp3 for mp3 in glob.glob(played_folder + "*.mp3", recursive=True)]
    for file in directory:
        shutil.move(file, song_folder)
    return


# Main control block as a function that is invoked off a physical button press
def dance_break():
    global i
    global song_folder
    global played_folder
    global playlist
    global media_status
    # If we already have a song playing, press the button and we will stop the music and return
    if pygame.mixer.music.get_busy():
        pygame.mixer.quit()
        print('Music Stopped!')
        sleep(1)
        pygame.mixer.init()
        return
    try:
        # check and update paths/playlist if we have added or removed usb storage
        location_handler()
        # play our 5MDB alert, the sleep starts the actual song at the appropriate time after the alert has played
        pygame.mixer.Sound(alert).play()
        sleep(8)
        # load up the next song to be played
        load_play()
    # If we can't load the next song check location and try to reset source
    except pygame.error:
        try:
            location_handler()
            load_play()
        except pygame.error:
            reset_played_dir()
            location_handler()
            load_play()
    # increase our index and if we have played the whole playlist, generate a new random playlist
    i += 1
    if len(playlist) - i == 0:
        reset_played_dir()
        playlist = build_playlist(song_folder)
        i = 0
        print('playlist reset Next song:', what_song(i))
        print(len(playlist) - i, 'songs left in playlist')
    else:
        print('Next song:', what_song(i))
        print(len(playlist) - i, 'songs left in playlist')
    return


# On load generate initial playlist
playlist = build_playlist()
# Listen for button press until program exit.
while True:
    button.when_pressed = dance_break
