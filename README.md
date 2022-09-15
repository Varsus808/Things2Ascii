# Things2Ascii

A CLI Tool to turn Videofeed, Picture- and Video Files into Ascii Characters, output to CLI.
Optimized for Linux.

## Installation
```sh
git clone https://github.com/Varsus808/ascii_cam.git
cd ascii_cam/
pip install -r requirements.txt
```

## Usage
```sh
Ascii Cam, example usage:
  python3 ascii_cam.py --cam -r 8 -color light_green
            --or--
  python3 ascii_cam.py --file /path/to/picture/or/video -r 8 -color light_green

options:
  -h, --help            show this help message and exit
  -c, --cam             VideoCapture Device -1
  -f FILE_PATH, --file FILE_PATH
                        Path to a Picture or Video
  -r RES, --resolution RES
                        Output resolution, starting at 0 (BIG) default 4
                        (inverse linear). Can be higher depending on your
                        input
  -o STORE, --output STORE
                        Name of Out File, currently supported for Picture Mode
  -col, --colour, --color 
                 choice from: black,red,green,orange,blue,purple,cyan,light_gray,dark_grey,
                 light_red,light_green,yellow,light_blue,light_purple,light_cyan,white
                        Color of Ascii chars, for bash console
  -a APPEARANCE, --appearance APPEARANCE
                        String of Ascii Characters to use in conversion
  -R RANDOM, --random RANDOM
                        Cycle through diffrent Ascii representation. Output
                        may seem broken at times, because random chars aren't
                        of equal width
  -s SOURCE, --source SOURCE
                        Provide index of Video Capture Device (e.g. default -1
                        for webcam)
```
