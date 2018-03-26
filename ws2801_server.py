import asyncio
import websockets
import RPi.GPIO as GPIO
#import time

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
PIXEL_COUNT = 96

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0

# Set the server port
PORT = 8000

# You can set DEBUG to True to receive logging on standard output.
#DEBUG = True
DEBUG = False

async def socketHandler(websocket, path):
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
          print(">> Initializing WS2801 strip...")
        pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

        # Clear all the pixels to turn them off.
        if DEBUG:
          print(">> Clearing all", PIXEL_COUNT, "pixels...")
        pixels.clear()
        pixels.show()  # Make sure to call show() after changing any pixels!

        # By default, we will automatically show what was sent. This can be overridden with the autoshow command.
        autoShow = True

        # The init command replies with the number of pixels on the strip.
        await websocket.send(str(pixels.count()))

      elif command == "clear":
        if DEBUG:
          print(">> Handling clear command")
        pixels.clear()
        if autoShow:
          pixels.show()

      elif command == "setpixel":
        if DEBUG:
          print(">> Handling setpixel command")
        pix = int(cmdList.pop(0))
        red = int(cmdList.pop(0))
        green = int(cmdList.pop(0))
        blue = int(cmdList.pop(0))
        pixels.set_pixel_rgb(pix, red, blue,green)
        if autoShow:
          pixels.show()

      elif command == "setpixels":
        if DEBUG:
          print(">> Handling setpixels command")
        red = int(cmdList.pop(0))
        green = int(cmdList.pop(0))
        blue = int(cmdList.pop(0))
        color=Adafruit_WS2801.RGB_to_color(red,blue,green)
        pixels.set_pixels(color)
        if autoShow:
          pixels.show()

      elif command == "shift":
        if DEBUG:
          print(">> Handling shift command")
        direction=cmdList.pop(0)
        if direction == "left":
          if DEBUG:
            print(">> Shifting left...")
          leftmostPixelColor = pixels.get_pixel(0)
          for pix in range(1, pixels.count()):
            color = pixels.get_pixel(pix)
            pixels.set_pixel(pix-1,color)
          pixels.set_pixel(pixels.count()-1,leftmostPixelColor)
          if autoShow:
            pixels.show()
        elif direction == "right":
          if DEBUG:
            print(">> Shifting right...")
          rightmostPixelColor = pixels.get_pixel(pixels.count()-1)
          for pix in reversed(range(1,pixels.count())):
            color = pixels.get_pixel(pix-1)
            pixels.set_pixel(pix,color)
          pixels.set_pixel(0,rightmostPixelColor)
          if autoShow:
            pixels.show()
        else:
          print(">> Unknown shift direction:", direction)

      elif command == "dim":
        if DEBUG:
          print(">> Handling dim command")
        step = int(cmdList.pop(0))
        for i in range(pixels.count()):
          red, green, blue = pixels.get_pixel_rgb(i)
          red = int(max(0, red - step))
          green = int(max(0, green - step))
          blue = int(max(0, blue - step))
          pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( red, green, blue ))
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
          print(">> Returning pixel count", pixels.count())
        await websocket.send(str(pixels.count()))

      else:
        print(">> Unknown command:", command)

  except websockets.exceptions.ConnectionClosed:
    if DEBUG:
      print("> Disconnected.")
  except:
    print("> Unknown exception encountered.")
    raise

start_server = websockets.serve(socketHandler, '0.0.0.0', PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
