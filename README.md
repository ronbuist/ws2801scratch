# ws2801scratch
A Scratch extension and python-based server for WS2801 led strips connected to a Raspberry Pi.

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
git clone https://github.com/ronbuist/ws2801scratch.git
ws2801/ws2801_server.py
```
The last command will start the server process which will wait for connections and then handle the commands that are being sent. It will run until you stop it with CTRL-C. If you're getting an error about Websockets not being installed, run the following:
```
sudo pip3 install websockets
```
Please take a look at ws2801_server.py. There are some configuration options in the beginning of the file. Please make sure you have set the amount of leds (pixels) your strip has (PIXEL_COUNT). Should you want to change the port number, please do so by changing the line that start with PORT=. Once everything is working as it should, you can run the program in the background using:
```
nohup python3 ws2801_server.py > ws2801_server.log 2>&1 & 
```
Alternatively, you could set the server up to run as a service on startup of the Raspberry Pi. That's beyond the scope of this document but there are lots of guides and tutorials available to figure out how to do this.

Please write down (or remember) the IP address of your Raspberry Pi; we will need it in the following steps...

### Making everything work together.
To load ScratchX with the WS2801 already installed, please point your browser to [http://scratchx.org/?url=https://ronbuist.github.io/ws2801/ws2801.js#scratch](http://scratchx.org/?url=https://ronbuist.github.io/ws2801/ws2801.js#scratch). As Scratch is based on Adobe Flash, you will need to have the Flash Player installed. If all goes as it should, you will receive a warning about the experimental nature of ScratchX extensions. Fair enough; just click the 'I understand, continue' button. After that, you should see the Scratch development environment, with somewhere in the middle the code blocks of the WS2801 extension. The 'light' next to ws2801 will be yellow, indicating that the extension is ready but is not connected yet. You are now ready to code the led strip in Scratch!

### Example Scratch programs.
I have created two example programs in Scratch that will demonstrate how to use the blocks to code the led strip:

1. [http://scratchx.org/?url=https://ronbuist.github.io/ws2801/GreenLights.sbx#scratch](http://scratchx.org/?url=https://ronbuist.github.io/ws2801/GreenLights.sbx#scratch). A simple example that connects to the server, sets all the pixels to bright green, waits 10 seconds and then closes the connection again. When the connection is closed, all the pixels will be switched off.
2. [http://scratchx.org/?url=https://ronbuist.github.io/ws2801/WS2801ColorWheel.sbx#scratch](http://scratchx.org/?url=https://ronbuist.github.io/ws2801/WS2801ColorWheel.sbx#scratch). This example program will set the strip to the colors of a color wheel and then shift the pixels left. You can change the direction with the arrow left and arrow right keys. Pressing the space bar will end the program, but not before dimming all the leds until they are all switched off.

In both examples, you will need to change the IP address and port number to match the ws2801_server.py process running on your Raspberry Pi. This is done in the 'Connect to WS2801 server' code block.

## Final note
Even though you most certainly can run Scratch in the Raspbian GUI, this is not required. The server process is using websockets and connections could come from everywhere in your network. This means you can open scratchx.org on a different computer and then connect to the server process on the Raspberry Pi. You don't even need to install the GUI in Raspbian. In my opinion, the Raspberry Pi is a great machine but not fast enough to run a graphical user interface.
