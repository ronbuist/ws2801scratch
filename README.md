# ws2801scratch
A Scratch extension and python-based server for WS2801 led stripes connected to Raspberry Pi

## Introduction
I wanted to create a way for my children to program a led strip using the popular [Scratch](http://scratch.mit.edu/) programming language for children. Even though there is lots of information and code to be found on programming the led strips in languages like C and Python, I could not find anything that connects the led strip to Scratch. This repository contains my solution to that...

## The ingredients
This is what I used:

* A Raspberry Pi 3B, running Raspbian Stretch.
* A WS2801 programmable led strip. Mine was 3 metres and contained 96 individual leds. Looking for your own strip? Aliexpress usually has some good deals on these.
* A 5V 6A power supply to power the leds.

## Why the WS2801?
I wanted to use the led strip in combination with a Raspberry Pi. The hugely popular WS2811 (Neopixel) strips are great, but need real-time controlling and that's something the Raspberry Pi cannot deliver. The WS2801 strips have an additional CLOCK (CLK) line, allowing the Raspberry Pi to control the pace of events.

## Setting things up; building on the work of others
Nowadays, there are so many great open source (scripting) languages, libraries and scripts to build upon and that's exactly what I did with my  project.

### Hardware: connecting the LED strip to the Raspberry Pi
This [excellent tutorial on tutorials-raspberrypi.com](https://tutorials-raspberrypi.com/how-to-control-a-raspberry-pi-ws2801-rgb-led-strip/) describes everything that is needed to connect the LED strip to the Raspberry Pi.

### Software: the Adafruit library
The tutorial mentioned above also describes installing the [Adafruit Python library](https://github.com/adafruit/Adafruit_Python_WS2801). I advice following the tutorials-raspberry.com tutorial and install the library using pip. In my case, I have used pip3 to install the library in Python 3.

Use the example in the tutorial to make sure you have everyting set up correctly before proceeding.

## Scratch extension and Python server

### A few words on architecture
The normal Scratch site on [scratch.mit.edu](http://scratch.mit.edu) does not allow using extensions. For that, a separate site on [scratchx.org](http://scratchx.org) is available. On ScratchX, you can import your own Scratch extension written in JavaScript. Once again, I managed to find [excellent documentation](https://github.com/LLK/scratchx/wiki) on how to create extensions. I didn't have any experience programming JavaScript, but with the example on LLK's page it wasn't that difficult to create the extension.

The extension works by connecting to a websocket on the server process running on the Raspberry Pi. Once connected, simple commands are used to interact with the led strip. For example:

```
setpixels 255 0 0
setpixel 0 0 255 0
shift right
```
The example above will first set all the lights on the strip to red (the numbers are RGB values). The second command will set the first pixel to green. After that, the pixels are shifted right, meaning in this case that the one green pixel will jump to the next pixel.

In Scratch, you don't need to worry about these commands; this is all handled by the extension. If you're interested, just take a look at the source code of the extension to see the commands that are sent to the server process.

### Running the server process
ws2801_server.py is the server process that runs on the Raspberry Pi to process the commands sent by the Scratch extension. To run it, do the following on the Raspberry Pi:

```
git clone 
```
