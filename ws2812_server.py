import asyncio
import websockets
import RPi.GPIO as GPIO
#import time

# Import the WS2812 module.
from neopixel import *

# Configure the count of pixels:
PIXEL_COUNT    = 75      # Number of pixels
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Set the server port
PORT = 8000

# You can set DEBUG to True to receive logging on standard output.
#DEBUG = True
DEBUG = False

# Some WS2812 strips use GRB for the color order. Set the color order using COLOR_ORDER.
#COLOR_ORDER = "RGB"
COLOR_ORDER = "GRB"

async def socketHandler(websocket, path):

  pixelCount=PIXEL_COUNT

  try:
    while True:
      cmdLine = await websocket.recv()
      cmdList = cmdLine.split(" ")
      command = cmdList.pop(0)
      if DEBUG:
        print("> Received command:", cmdLine)

      # Process the command
      if command == "init":
        # Initialize the led strip.
        if DEBUG:
          print(">> Initializing WS2812 strip...")
        pixels = Adafruit_NeoPixel(PIXEL_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        pixels.begin()

        # Clear all the pixels to turn them off.
        if DEBUG:
          print(">> Clearing all", PIXEL_COUNT, "pixels...")
        for pix in range(pixels.numPixels()):
          pixels.setPixelColor(pix,0)
        pixels.show()  # Make sure to call show() after changing any pixels!

        # By default, we will automatically show what was sent. This can be overridden with the autoshow command.
        autoShow = True

        # The init command replies with the number of pixels on the strip.
        await websocket.send(str(pixels.numPixels()))

      elif command == "clear":
        if DEBUG:
          print(">> Handling clear command")
        for pix in range(pixels.numPixels()):
          pixels.setPixelColor(pix,0)
        if autoShow:
          pixels.show()

      elif command == "setpixel":
        if DEBUG:
          print(">> Handling setpixel command")
        pix = int(cmdList.pop(0))
        red = int(cmdList.pop(0))
        green = int(cmdList.pop(0))
        blue = int(cmdList.pop(0))
        if pixelCount < PIXEL_COUNT:
          # Handle virtual split into multiple strips
          while pix < PIXEL_COUNT:
            if COLOR_ORDER == "RGB":
              pixels.setPixelColorRGB(pix, red, green, blue)
            else:
              pixels.setPixelColorRGB(pix, green, red, blue)
            pix = pix + pixelCount
        else:
          if COLOR_ORDER == "RGB":
            pixels.setPixelColorRGB(pix, red, green,blue)
          else:
            pixels.setPixelColorRGB(pix, green, red, blue)
        if autoShow:
          pixels.show()

      elif command == "setpixels":
        if DEBUG:
          print(">> Handling setpixels command")
        red = int(cmdList.pop(0))
        green = int(cmdList.pop(0))
        blue = int(cmdList.pop(0))
        for pix in range(pixels.numPixels()):
          if COLOR_ORDER == "RGB":
            pixels.setPixelColorRGB(pix, red, green,blue)
          else:
            pixels.setPixelColorRGB(pix, green, red, blue)
        if autoShow:
          pixels.show()

      elif command == "shift":
        if DEBUG:
          print(">> Handling shift command")
        direction=cmdList.pop(0)
        if direction == "left":
          if DEBUG:
            print(">> Shifting left...")
          leftmostPixelColor = pixels.getPixelColor(0)
          if pixelCount < PIXEL_COUNT:
            if DEBUG:
              print(">>Handling virtual pixels for", pixelCount, "virtual pixels over",PIXEL_COUNT,"real pixels")
            nrIterations = PIXEL_COUNT // pixelCount
            for i in range(0, nrIterations):
              for pix in range(1, pixelCount):
                color = pixels.getPixelColor(i*pixelCount+pix)
                pixels.setPixelColor(i*pixelCount+pix-1,color)
              pixels.setPixelColor((i+1)*pixelCount-1,leftmostPixelColor)
            if PIXEL_COUNT % pixelCount > 0:
              i = 0
              for pix in range(nrIterations*pixelCount,PIXEL_COUNT):
                color = pixels.getPixelColor(i)
                pixels.setPixelColor(pix,color)
                i = i + 1
          else:
            for pix in range(1, pixels.numPixels()):
              color = pixels.getPixelColor(pix)
              pixels.setPixelColor(pix-1,color)
            pixels.setPixelColor(pixels.numPixels()-1,leftmostPixelColor)
          if autoShow:
            pixels.show()
        elif direction == "right":
          if DEBUG:
            print(">> Shifting right...")
          rightmostPixelColor = pixels.getPixelColor(pixelCount-1)
          if pixelCount < PIXEL_COUNT:
            if DEBUG:
              print(">>Handling virtual pixels for", pixelCount, "virtual pixels over",PIXEL_COUNT,"real pixels")
            nrIterations = PIXEL_COUNT // pixelCount
            if PIXEL_COUNT % pixelCount > 0:
              for pix in reversed(range(nrIterations*pixelCount,PIXEL_COUNT)):
                color = pixels.getPixelColor(pix-1)
                pixels.setPixelColor(pix,color)
            for i in range(0, nrIterations):
              for pix in reversed(range(1, pixelCount)):
                color = pixels.getPixelColor(i*pixelCount+pix-1)
                pixels.setPixelColor(i*pixelCount+pix,color)
              pixels.setPixelColor(i*pixelCount,rightmostPixelColor)
          else:
            for pix in reversed(range(1,pixels.numPixels())):
              color = pixels.getPixelColor(pix-1)
              pixels.setPixelColor(pix,color)
            pixels.setPixelColor(0,rightmostPixelColor)
          if autoShow:
            pixels.show()
        else:
          print(">> Unknown shift direction:", direction)

      elif command == "dim":
        if DEBUG:
          print(">> Handling dim command")
        step = int(cmdList.pop(0))
        for i in range(pixels.numPixels()):
          color = pixels.getPixelColor(i)
          red = (color >> 16) & 0xFF
          green = (color >> 8) & 0xFF
          blue = color & 0xFF

          red = int(max(0, red - step))
          green = int(max(0, green - step))
          blue = int(max(0, blue - step))

          pixels.setPixelColorRGB(i,red,green,blue)
        if autoShow:
          pixels.show()

      elif command == "autoshow":
        if DEBUG:
          print(">> Handling autoshow command")
        state = cmdList.pop(0)
        if state == "on":
          autoShow = True
        elif state == "off":
          autoShow = False
        else:
          print(">> Unknown state for autoshow:", state)

      elif command == "show":
        if DEBUG:
          print(">> Handling show command")
        pixels.show()

      elif command == "getpixelcount":
        if DEBUG:
          print(">> Handling getpixelcount command")
          print(">> Returning pixel count", pixels.numPixels())
        await websocket.send(str(pixels.numPixels()))

      elif command == "setVirtualPixels":
        if DEBUG:
          print(">> Handling setVirtualPixels")
        nrPixels = int(cmdList.pop(0))
        pixelCount = nrPixels

      else:
        print(">> Unknown command:", command)

  except websockets.exceptions.ConnectionClosed:
    if DEBUG:
      print("> Disconnected.")
  except:
    print("> Unknown exception encountered.")
    raise

print("WS2812 server starting...")
start_server = websockets.serve(socketHandler, '0.0.0.0', PORT)

print("> Websocket initialized. Now entering main loop...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
