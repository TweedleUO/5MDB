# Five Minute Dance Break

5MDB is a part of Apox Wow camp bondage.  

It runs on a raspberry pi and uses a physical button to trigger an alarm, then plays a song from a playlist.

Playlists can be generated from .mp3s loaded locally on the device or from a flash drive.
## Installation
Raspbian comes pre-loaded with pygame and GPIO Zero.  If you need to install them on a different distro or want more information see dependency section at the end of README
1. Create the following folders (or your own custom folders):
```bash
mkdir /home/pi/code/5MDB/
```
```bash
mkdir /home/pi/code/5MDB/playlist/
```
```bash
mkdir /home/pi/code/5MDB/playled/
```
2. Wire a button to your GPIO 10 pin (or any available pin)
   

3. Copy dance.py and alarm.wav to your .../5MDB/ folder
   

4. If you customized your path or GPIO pin, update the variables:
```python
button = Button(YOUR_GPIO_PIN_NUMBER)
alert = YOUR_PATH/alarm.wav
song_folder = YOUR_SONG_FOLDER_PATH
played_folder = YOUR_PLAYED_FOLDER_PATH
```

5. Execute dance.py, or add the following to rc.local to run it at startup:
```bash
python3 /home/pi/code/5MDB/dance.py &
```
Optional:
6. If using a flash drive create the following folders:
```bash
/5MDB/
```
```bash
/5MDB/played
```
```bash
/5MDB/playlist
```
In the final 'playlist' directory load all your .mp3 files

## Dependencies
To install pygame:
```bash
python3 -m pip install pygame==1.9.6
```
pygame 2.x required additional dependencies at the time of writing and didn't offer any additional needed functionality.
https://www.pygame.org/wiki/GettingStarted

To install GPIO Zero:
```bash
sudo apt install python3-gpiozero
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)