# Pi MIDI Display - an LED MIDI visualizer


The Pi MIDI Display is a set of hardware and software that creates a visual display from an
RGB LED Matrix to represent incoming MIDI note data. It was originally developed to accompany a MIDI
controlled Eurorack modular synthesizer so the audience could visually connect the incoming notes 
to the activity of the synth.

Each row of an LED matrix is assigned a starting midi note value.
By defualt row starting values are offset by a 4th. This offset can be redefined if desired.
Each pitch class is represented by a specific color value. These are also changeable.
When a MIDI note on is received the note is added to a list of current notes.
When a MIDI note off is received the note is removed from the list of current notes.
After each MIDI event highlight the current note coordinates with the appropriate pitch class color.

## Dependencies

### Hardware
- RPi 3B+ or greater
- Raspian OS
- Adafruit RGB Matrix Hat or Bonnet
- An LED Matrix 16x32 up to 64x64 as supported by the Matrix Hat. This code was tested on a 16x32 LED Matrix
- A MIDI interface for receiving MIDI data

### Firmware
- RGBMatrix libraries 
  - https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices
  - https://github.com/hzeller/rpi-rgb-led-matrix

### Additional libraries
- mido
- python-rtmidi
- libasound2-dev
- libjack-dev

## Installation
>TODO: Create a simple installation script to add a dependencies to a new installation

MIDI libs installation notes:
```
sudo pip3 install mido
sudo apt-get install libasound2-dev
sudo apt-get install libjack-dev
sudo pip3 install python-rtmidi
```
make sure root is added to the audio group for midi to work properly
```
$ sudo usermod -a -G audio root
```