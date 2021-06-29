# Five Minute Dance Break

5MDB is a part of Apox Wow camp bondage.  

It runs on a raspberry pi and uses a physical button to trigger an alarm, then plays a song from a playlist.

Playlists can be generated from .mp3s loaded locally on the device or from a flash drive.
## Installation
Raspbian comes pre-loaded with pygame and GPIO Zero.  If you need to install them on a different distro or want more information see dependency section at the end of README
1. Download the latest release zip file from release tab


2. Unzip folder in your home directory ~/ (/home/pi/)
note: if your user is not `pi` then update the variables in step 6 accordingly.


3. Wire a button to GPIO pin 10

Optional:
4. For use with a flash drive create a 5MDB folder at the root and then create a `playlist` and `played` subfolder. Load your mp3s into the `playlist` folder.


5. To run 5MDB at startup add the following line to your rc.local:
```bash
python3 /home/pi/5MDB/dance.py &
``` 
6. To customize your instalation path or GPIO pin, update the variables:
```python
button = Button(YOUR_GPIO_PIN_NUMBER)
alert = YOUR_PATH/alarm.wav
song_folder = YOUR_SONG_FOLDER_PATH
played_folder = YOUR_PLAYED_FOLDER_PATH
```

## Dependencies
You may need to install usbmount if running this headless:
```bash
sudo apt-get install -y usbmount
```

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