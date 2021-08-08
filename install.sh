#!/usr/bin/env bash

install_rgb_matrix () {
  echo 'installing rgb-matrix from AdaFruit'
  curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
  sudo bash rgb-matrix.sh
}

install_midi_stack () {
  echo 'installing midi dependencies'
  # should we check to see if rtmidi is already installed ?
  sudo pip3 install mido
  sudo apt-get install libasound2-dev
  sudo apt-get install libjack-dev
  sudo pip3 install python-rtmidi
}

add_root_to_audio () {
  echo 'adding root to audio group'
  sudo usermod -a -G audio root
}

start_pi_display_at_login () {
  echo 'setting up pi midi display to start at login'
}


__welcome_message="
This script will install the following things to your Raspberry Pi:
  - rgb-matrix -- from Adafruit and hzeller
  - mido python -- library
  - python-midi -- python library
  - libasound2-dev -- linux audio library
  - libjack-dev -- linux audio library
  - pi-midi-display -- firmware

it will also add your root user to the audio group
"

get_started () {
  echo "$__welcome_message"
  read -p "is this ok?" -n 1 -r
  echo # move to the next line
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    # install things
    install_rgb_matrix
    install_midi_stack
    add_root_to_audio

    read -p "Do you want the pi-midi-display to auto start after login?" -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
      start_pi_display_at_login
    fi
    
  fi
}

get_started
