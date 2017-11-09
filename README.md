

https://gamemechanicexplorer.com/
http://www.nerdparadise.com/programming/pygamejoystick

Debug Build (as folder and with console)
```
pyinstaller .\main.py --add-data ".\img;img" --add-data ".\map;map"
```


Release Build (as single exe, windowed)
```
pyinstaller .\main.py -F --add-data ".\img;img" --add-data ".\map;map" --add-data ".\snd;snd" --windowed
```
