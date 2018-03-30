/**
 Copyright (c) 2018 Ron Buist All right reserved.
 WS2801 Scratch extension is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

(function (ext) {
    var socket = null;

    var connected = false;
    var myStatus = 1;						// initially, set light to yellow
    var myMsg = 'not_ready';
    var pixelCount = 0;

    // General functions.
    function colorLimit(color) {
        color = parseInt(color);
        color = Math.min(255,color);
        color = Math.max(0,color);
        return color;
    };

    // when the connect to server block is executed.
    ext.cnct = function (hostname, port, callback) {
        window.socket = new WebSocket("ws:" + hostname + ":" + String(port));
        window.socket.onopen = function () {

            // initialize the led strip
            window.socket.send("init");

        };

        // Onmessage handler to receive the result. The result is the number of pixels,
        // which we will store in a variable.
        window.socket.onmessage = function (message) {

            // store the number of pixels on the strip.
            pixelCount = parseInt(message.data);

            // change status light from yellow to green.
            myMsg = 'ready';
            connected = true;
            myStatus = 2;

            // Callback to let Scratch know initialization is complete.
            callback();
        };

        window.socket.onclose = function (e) {
            console.log("Connection closed.");
            socket = null;
            connected = false;
            myMsg = 'not_ready'; // back to yellow status.
            myStatus = 1;
        };
    };

    // Cleanup function when the extension is unloaded
    ext._shutdown = function () {
        var msg = "clear";
        window.socket.send(msg);
        window.socket.onclose = function () {}; // disable onclose handler first
    	window.socket.close(); // close the socket.
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function (status, msg) {
        return {status: myStatus, msg: myMsg};
    };

    // when the clear all pixels block is executed
    ext.clearPixels = function () {
        if (connected == false) {
            alert("Server Not Connected");
        }
        window.socket.send("clear");
    };

    // when the set all pixels block is executed
    ext.setPixels = function (red, green,blue) {
        red = colorLimit(red);
        green = colorLimit(green);
        blue = colorLimit(blue);
    	var msg = "setpixels " + String(red) + " " + String(green) + " " + String(blue);
    	window.socket.send(msg);
    };

    // when the set pixel block is executed
    ext.setPixel = function (pixel, red, green, blue) {
        if (pixel >= 0 && pixel <= pixelCount) {
          red = colorLimit(red);
          green = colorLimit(green);
          blue = colorLimit(blue);
          var msg = "setpixel " + String(pixel) + " " + String(red) + " " + String(green) + " " + String(blue);
    	  window.socket.send(msg);
        }
    };

    // when the autoshow block is executed
    ext.autoShow = function (autoShowValue) {
        if (autoShowValue == "On" || autoShowValue == "Aan") {
          window.socket.send("autoshow on");
        } else {
          window.socket.send("autoshow off");
    	}
    };

    // when the show block is executed
    ext.show = function () {
    	window.socket.send("show");
    };

    // when the shift block is executed
    ext.shiftPixels = function (direction) {
    	if (direction == "Left" || direction == "Links") {
    		window.socket.send("shift left");
    	} else {
    		window.socket.send("shift right");
    	}
    };

    // when the dim block is executed
    ext.dim = function (dimAmount) {
      dimAmount = Math.ceil(dimAmount);
      dimAmount = colorLimit(dimAmount);
      var msg = "dim " + String(dimAmount);
      window.socket.send(msg);
    };

    // when the disconnect from server block is executed
    ext.discnct = function () {
        var msg = "clear";
        window.socket.send(msg);
        window.socket.onclose = function () {}; // disable onclose handler first
    	window.socket.close();                  // close the socket.
    	socket = null;
        connected = false;
        myMsg = 'not_ready';                    // back to yellow status.
        myStatus = 1;
        pixelCount = 0;
    };

    // when the number of pixels reporter block is executed
    ext.getPixelCount = function() {

       // The number of pixels on the strip was already determined at initialization.
       // Just return that number here...
       return pixelCount;

    };

    // Block and block menu descriptions
    var lang = navigator.language || navigator.userLanguage;
    lang = lang.toUpperCase();
    if (lang.includes('NL')) {

        var descriptor = {
            blocks: [
                // Block type, block name, function name
                ["w", 'Verbind met WS2801 server op %s poort %n.', 'cnct', "Host", "Poort"],
                [" ", 'Verbreek verbinding met WS2801 server', 'discnct'],
                [" ", 'Alle pixels uit', 'clearPixels'],
                [" ", 'Kleur alle pixels rood %n groen %n blauw %n', 'setPixels', "0", "0", "0"],
                [" ", 'Kleur pixel %n rood %n groen %n blauw %n', 'setPixel', "0", "0", "0", "0"],
                [" ", 'Direct zien %m.showstate', 'autoShow', "Aan"],
                [" ", 'Toon pixels', 'show'],
                [" ", 'Verschuif pixels %m.direction', 'shiftPixels', "Links"],
                [" ", 'Maak pixels %n donker', 'dim', "1"],
                ["r", 'Aantal pixels','getPixelCount']
            ],
            "menus": {
                "direction": ["Links", "Rechts"],
                "showstate": ["Aan", "Uit"]

            },
            url: 'https://github.com/ronbuist/ws2801scratch'
        };

    }
    else {

        var descriptor = {
            blocks: [
                // Block type, block name, function name
                ["w", 'Connect to WS2801 server on host %s and port %n.', 'cnct', "Host", "Port"],
                [" ", 'Disconnect from WS2801 server', 'discnct'],
                [" ", 'Clear All Pixels', 'clearPixels'],
                [" ", 'Set All Pixels to color red %n green %n blue %n', 'setPixels', "0", "0", "0"],
                [" ", 'Set pixel %n to color red %n green %n blue %n', 'setPixel', "0", "0", "0", "0"],
                [" ", 'Autoshow %m.showstate', 'autoShow', "On"],
                [" ", 'Show pixels', 'show'],
                [" ", 'Shift pixels %m.direction', 'shiftPixels', "Left"],
                [" ", 'Dim pixels %n', 'dim', "1"],
                ["r", 'number of pixels','getPixelCount']
            ],
            "menus": {
                "direction": ["Left", "Right"],
                "showstate": ["On", "Off"]

            },
            url: 'https://github.com/ronbuist/ws2801scratch'
        };
    };

    // Register the extension
    ScratchExtensions.register('ws2801', descriptor, ext);
})({});
