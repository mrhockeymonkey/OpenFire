This project was started for the purpose of learning python and having some fun along the way. This is a largely unfinished project, however it has become apparent that for the kind of game I want to create PyGame is not the right choice of engine [link](https://www.pygame.org/docs/tut/newbieguide.html). In the future I plan to pick up some C# and have another go at creating a hectic hack'n'slash game in something like unity. 

Credits:
* kidscancode.org for detailed walkthroughs of how to use pygame - http://kidscancode.org/lessons/
* kenny for top quilty isometric tiles - https://kenney.itch.io/kenney-game-assets-3
* luis mullmann for some fantastic python code around polygons - https://hackmd.io/s/ryFmIZrsl
* pygame.org for a great sprite animation class - https://www.pygame.org/wiki/Spritesheet
* GameMechanicExplorer.com for help with animations - https://gamemechanicexplorer.com/
* Ner Paradise for some yet unsused joystick code - http://www.nerdparadise.com/programming/pygamejoystick


Debug Build (as folder and with console)
```
pyinstaller .\main.py --noconfirm --add-data ".\img;img" --add-data ".\map;map" --add-data ".\snd;snd"
```

Release Build (as single exe, windowed)
```
pyinstaller .\main.py -F --noconfirm --add-data ".\img;img" --add-data ".\map;map" --add-data ".\snd;snd" --windowed
```


