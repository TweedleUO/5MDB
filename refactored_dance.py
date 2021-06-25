#!/usr/bin/python3
import glob, shutil, random, pygame
from gpiozero import Button
from time import sleep
from os import path

pygame.mixer.init()
button = Button(10)
alert = '/home/pi/5MDB/alarm.wav'
hal9000 = '/home/pi/5MDB/icant.wav'
song_folder = ''
played_folder = ''
playlist = None
media_status = None
i = 0

def check_removable_media():
    r_playlist = glob.glob('/media/pi/*/5MDB/playlist/')
    r_played = glob.glob('/media/pi/*/5MDB/played/')
    if len(r_playlist) > 0 and len(r_played) > 0:
        return True
    return False

def build_playlist(upcoming=song_folder):
    pl = [mp3 for mp3 in glob.glob(upcoming + "*.mp3", recursive=True)]
    random.shuffle(pl)
    return pl

def store_path():
    global song_folder
    global played_folder
    validator = song_folder
    if check_removable_media():
        #extra variable to account for multiple found removable media entries
        s_folder = glob.glob('/media/pi/*/5MDB/playlist/')
        song_folder = s_folder[0]
        p_folder = glob.glob('/media/pi/*/5MDB/played/')
        played_folder = p_folder[0]
    else:
        song_folder = '/home/pi/5MDB/playlist/'
        played_folder = '/home/pi/5MDB/played/'
    if validator == song_folder:
        print('No Change' + song_folder)
        return 
    else:
        print('Updated' + str(song_folder))
        return

def location_handler():
    global song_folder
    global i
    global playlist
    if check_removable_media() and song_folder == '/home/pi/5MDB/playlist/':
        print('new media detected, updating')
        store_path()
        playlist = build_playlist()
        i = 0
        print('now reading from external drive')
        return
    elif not check_removable_media() and song_folder != '/home/pi/5MDB/playlist/':
        print('media removed, updating')
        store_path()
        playlist = build_playlist()
        i = 0
        print('now reading from local drive')
        return
    print('media source all good')
    return

def load_play():
    global i
    global playlist
    global played_folder
    print('Now playing:',what_song(i))
    try:
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        shutil.move(playlist[i],played_folder)
        return
    except IndexError:
        reset_played_dir()
        location_handler()
        pygame.mixer.music.load(playlist[i])
        pygame.mixer.music.play()
        shutil.move(playlist[i],played_folder)

def what_song(index):
    global playlist
    global played_folder
    this_song = playlist[index]
    return path.basename(this_song.strip('.mp3'))

def reset_played_dir():
    global song_folder
    global played_folder
    directory = [mp3 for mp3 in glob.glob(played_folder + "*.mp3", recursive=True)]
    for file in directory:
        shutil.move(file,song_folder)
    return

def dance_break():
    global i
    global song_folder
    global played_folder
    global playlist
    global media_status
    location_handler()
    if pygame.mixer.music.get_busy():
        pygame.mixer.quit()
        print('Music Stopped!')
        sleep(1)
        pygame.mixer.init()
        return
    try:
        pygame.mixer.Sound(alert).play()
        sleep(8)
        load_play()
    except pygame.error:
        try:
            location_handler()
            load_play()
        except pygame.error:
            reset_played_dir()
            location_handler()
            load_play()
            
    i += 1
    if len(playlist)-i == 0:
        reset_played_dir()
        playlist = build_playlist()
        i = 0
        print('playlist reset Next song:',what_song(i))
        print(len(playlist)-i, 'songs left in playlist')
    else:
        print('Next song:',what_song(i))
        print(len(playlist)-i, 'songs left in playlist')
    return

playlist = build_playlist()
button.when_pressed = dance_break

        
    