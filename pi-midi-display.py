#!/usr/bin/env python3

# Pi MIDI Display - a MIDI LED visualizer
#
# Dependencies:
# mido
# rtmidi
# RPi 3B+ or greater
# Adafruit RGB Matrix Hat or Bonnet
# An LED Matrix 16x32 up to 64x64 as supported by the Matrix Hat. This code was tested on a 16x32 LED Matrix
# rgb matrix libraries https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices
# A MIDI interface for receiving MIDI data
#
# MIDI libs installation:
# sudo pip3 install mido
# sudo apt-get install libasound2-dev
# sudo apt-get install libjack-dev
# sudo pip3 install python-rtmidi
#
# make sure root is added to the audio group for midi to work properly
# $ sudo usermod -a -G audio root
#

import sys
import time

import mido
from rgbmatrix import RGBMatrix, RGBMatrixOptions

class PiMidiDisplay():
  """
  Pi MIDI Display - an LED MIDI visualizer
    Author: t@creativecontrol.cc
  
  Each row of an LED matrix is assigned a starting midi note value.
  By defualt row starting values are offset by a 4th. This offset can be redefined if desired.
  Each pitch class is represented by a specific color value. These are also changeable.
  When a MIDI note on is received the note is added to a list of current notes.
  When a MIDI note off is received the note is removed from the list of current notes.
  After each MIDI event highlight the current note coordinates with the appropriate pitch class color.
  """
  def __init__(self):
    # Instance variables
    self.led_test = False # When True runs a sequence over all pitch classes to preview mapping of notes
    self.midi_print = False # prints all incoming messages that aren't note on/off

    self.midi_input_device = 'Deluge:Deluge MIDI 1 20:0'
    self.led_rows = 16
    self.led_cols = 32
    self.hardware = "adafruit-hat"
    self.brightness = 65
    self.x_count = 0
    self.y_count = 0

    self.row_map_start_note = 14
    # Row offset is in half-steps i.e. 4 = P4, 7 = P5, 12 = P8
    self.row_map_offset = 5
    # direction options 'top_bottom' and 'bottom_top'
    self.row_map_direction = 'bottom_top'

    self.colors = {
      'c': '#EE2902' , 
      'c#': '#ee9602',
      'd': '#02c7ee',
      'd#': '#0259ee',
      'e': '#ee0251',
      'f': '#ee2102',
      'f#': '#ee9f02',
      'g': '#cfee02',
      'g#': '#c7ee02',
      'a': '#59ee02',
      'a#': '#02ee29',
      'b': '#02ee97'
    }

    # End of Instance variables

    self.pitch_classes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

    self.test_sequence = self.pitch_classes

    options = RGBMatrixOptions()
    options.rows = self.led_rows
    options.cols = self.led_cols
    options.hardware_mapping = self.hardware
    options.brightness = self.brightness

    self.matrix = RGBMatrix(options = options)

    # Row map format, built programmatically
    # self.row_map = [119, 112, 105, 98, 91, 84, 77, 70, 63, 56, 49, 42, 35, 28, 21, 14]
    self.row_map = []

    self.current_notes = []

  def build_row_map(self):
    map = []
    for i in range(0,self.led_rows):
      map.append(self.row_map_start_note + (self.row_map_offset*i))
    if self.row_map_direction == 'bottom_top':
      map.reverse()

    self.row_map = map
    print(f'row mapping {self.row_map}')

  def init_midi(self):
    self.inport = mido.open_input(self.midi_input_device, callback=self.handle_midi_message)
    if self.inport:
      print(f'Connected to MIDI device {self.inport.name}')
  
  def handle_midi_message(self, msg):
    # print(msg)
    if msg.type == 'note_on':
      self.handle_note_on(msg)
    elif msg.type == 'note_off':
      self.handle_note_off(msg)
    else:
      if self.midi_print:
        print(msg)
      

  def handle_note_on(self, msg):
    if (msg.note not in self.current_notes):
      self.current_notes.append(msg.note)
      self.update_pixels()

  def handle_note_off(self, msg):
    if (msg.note in self.current_notes):
      self.current_notes.remove(msg.note)
      self.update_pixels()

  def hex_to_rgb(self, value: str) -> tuple:
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
  
  def midi_to_pitch_class(self, midi_note: int) -> str:
    pitch_class = self.pitch_classes[midi_note % 12]
    return pitch_class

  def where_in_rows(self, midi_note: int) -> list:
    """
    Searches for the incoming midi_note in each row
    If it is there it returns its coordinates
    """
    rows = []
    for row, start_note in enumerate(self.row_map):
      if midi_note >= start_note:
        column = midi_note - start_note
        rows.append({'x': column, 'y': row})
    return rows 

  def update_pixels(self):
    self.offset_canvas.Clear()
    for note in self.current_notes:
      pixels = self.where_in_rows(note)
      note_color = self.hex_to_rgb(self.colors[self.midi_to_pitch_class(note)])

      for pixel in pixels: 
        self.offset_canvas.SetPixel(pixel['x'], pixel['y'], note_color[0], note_color[1], note_color[2])

    self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
    

  def run(self):
    print("Running")

    self.build_row_map()
    self.init_midi()
    self.offset_canvas = self.matrix.CreateFrameCanvas()

    if self.led_test:
      self.test_matrix
    else:
      while True:
        pass
  
  def clearCanvas(self):
    self.offset_canvas.Clear()
    self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)

  
  def test_matrix(self):
    while True:
        for pitch in self.test_sequence:
          print(f'test pitch: {pitch}')
          pixel_update = []
          note_color = self.hex_to_rgb(self.colors[pitch])
          for row in range(0, self.led_rows):
            row_start = self.row_map[row]  
            for col in range(0, self.led_cols):
              if self.pitch_classes[(row_start+col)%12] == pitch:
                pixel_update.append({'x': col, 'y': row})

          self.offset_canvas.Clear()
            
          for pixel in pixel_update:
            self.offset_canvas.SetPixel(pixel['x'], pixel['y'], note_color[0], note_color[1], note_color[2])
          self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
          time.sleep(0.1)
          
  def process(self):
    try:
      print("Press Ctrl+C to stop")
      self.run()
    except KeyboardInterrupt:
      print("\nExiting\n")
      self.inport.close()
      self.clearCanvas()
      sys.exit(0)
    return True
        
# Main function
if __name__ == "__main__":
  midi_display = PiMidiDisplay()
  print(midi_display.__doc__)
  midi_display.process()