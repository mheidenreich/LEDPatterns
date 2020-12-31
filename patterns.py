#!/usr/bin/python3

"""
    Program: LED Patterns (patterns.py)
    Author:  M. Heidenreich, (c) 2020

    Description: This code is provided in support of the following YouTube tutorial:
                 https://youtu.be/bUaq-MoaPk0 

                 This example demonstrates how to use Raspberry Pi to blink multiple patterns using multiple LEDs.  

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import LED, Button
from threading import Thread
from time import sleep
from random import randrange

patterns = (
                [1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0]
            )
leds = (LED(20), LED(21), LED(26), LED(19), LED(13), LED(6))
button = Button(16)

is_running = True
delay = 0.1

index = 0
led_in = 5
led_out = 0

def safe_exit(signum, frame):
    exit(1)

def show_pattern():
    while is_running:
        for id in range(6):
            leds[id].value = patterns[index][id]

        token = patterns[index].pop(led_out)
        patterns[index].insert(led_in, token)

        sleep(delay)

def change_direction():
    global led_in, led_out, index

    led_in, led_out = led_out, led_in

    while True:
        new_index = randrange(0, len(patterns))

        if new_index != index:
            index = new_index
            break
try:

    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    button.when_pressed = change_direction
    index = randrange(0, len(patterns))

    worker = Thread(target=show_pattern, daemon=True)
    worker.start()

    pause()

except KeyboardInterrupt:
    pass

finally:
    is_running = False
    sleep(1.5*delay)

    for id in range(6):
        leds[id].close()
