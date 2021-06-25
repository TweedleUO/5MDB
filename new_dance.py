#!/usr/bin/python3
import glob, shutil, random
from gpiozero import Button
from time import sleep
from pygame import mixer, error as pgerror

#initialization block.  Load audio player, RPI button controller on GPIO #10 and set paths for audio files
mixer.init()
button = Button(10)
# song_folder = '/home/pi/5MDB/playlist/'
# played_song_folder = '/home/pi/5MDB/played/'
alert = '/home/pi/5MDB/alarm.wav'
hal9000 = '/home/pi/5MDB/icant.wav'

#Override system default with removable media if it exists
def find_removable_media():
    r_playlist = glob.glob('/media/pi/*/5MDB/playlist/')
    r_played = glob.glob('/media/pi/*/5MDB/played/')
    print(r_playlist,r_played)
    if r_playlist != [] and r_played != []:
        return r_playlist[0],r_played[0]
    return '/home/pi/5MDB/playlist/','/home/pi/5MDB/played/'
    

# Searches playlist directory (path) for all mp3s then populates playlist from that
def build_playlist():
    playlist = [mp3 for mp3 in glob.glob(song_folder + "*.mp3", recursive=True)]
    # If the directory is empty move played directory and rebuild
    if len(playlist) == 0:
        reset_files()
        playlist = [mp3 for mp3 in glob.glob(song_folder + "*.mp3", recursive=True)]
        if len(playlist) == 0:
            return None
    random.shuffle(playlist)
    print('playlist built')
    print(playlist[0].strip(song_folder),'is first up')
    return playlist
# Define our playlist variable by calling build function
song_folder,played_song_folder = find_removable_media()
playlist = build_playlist()

def bootstrap():
    print('bootstrap called, blow it up and start again')
    global i
    i = 0
    reset_files()
    global playlist
    playlist = build_playlist()

# Set index for playlist[i] and enter while loop to detect button press
i = 0
while True:
    # When button is pushed trigger music stop, play alert, play next song and move it to played folder
    if playlist == None:
        print(playlist)
        mixer.Sound(hal9000).play()
        break
    elif button.is_pressed and mixer.music.get_busy() == 1:
        mixer.music.stop()
        print("Music stopped")
        sleep(1) #this prevents multiple executes on a slow button push
    elif button.is_pressed and mixer.music.get_busy() == 0:
        try:
            mixer.Sound(alert).play()
            print('Alert played')
            sleep(8)  # This let's the alert play before loading the actual song
            mixer.music.load(playlist[i])
            mixer.music.play()
            print(playlist[i].strip(song_folder), 'now playing')
            justplayed = played_song_folder + playlist[playlist_index].strip(song_folder)
            shutil.move(playlist[i], justplayed)
            print(playlist[i].strip(song_folder), 'moved to played folder')
            i += 1
            if i == len(playlist):
                print('Last song in playlist, reshuffling songs')
                directory = [mp3 for mp3 in glob.glob(played_song_folder + "*.mp3", recursive=True)]
                for file in directory:
                    moveback = song_folder + file.strip(played_song_folder)
                    shutil.move(file, moveback)
                print('Played files moved back to main directory')
                playlist = [mp3 for mp3 in glob.glob(song_folder + "*.mp3", recursive=True)]
                i = 0
            else:
                print(playlist[i].strip(song_folder), 'is up next')
        # This exception would occur if a file is unable to be loaded.        
        except pgerror:
            i = 0
            print('Unable to load song, rebuilding playlist')
            playlist = [mp3 for mp3 in glob.glob(song_folder + "*.mp3", recursive=True)]
            try:
                play_music(i)
                move_file(i)
                i += 1
                try:
                    print(playlist[i].strip(song_folder), 'is up next')
                except IndexError:
                    bootstrap()
            except TypeError: #fall back on default or new path
              song_folder,played_song_folder = find_removable_media() 