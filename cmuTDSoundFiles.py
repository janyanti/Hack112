# GAME SOUNDS & MUSIC

from pygame import *

mixer.init()


def buttonPress():
    buttonPress = mixer.Sound('assets/beep-07.wav')
    mixer.Sound.set_volume(buttonPress, 0.2)
    buttonPress.play()


def balloonPop():
    balloonPop = mixer.Sound('assets/balloonPop.wav')
    mixer.Sound.set_volume(balloonPop, 0.75)
    balloonPop.play()


def playMusic():
    mixer.music.load('assets/bgMusic.mp3')
    mixer.music.play()


def continueMusic():
    if not mixer.music.get_busy():
        mixer.music.rewind()
        mixer.music.play()
