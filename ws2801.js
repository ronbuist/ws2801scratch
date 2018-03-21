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

    ext.cnct = function (hostname, port, callback) {
        window.socket = new WebSocket("ws:" + hostname + ":" + String(port));
        window.socket.onopen = function () {

			// change status light from yellow to green.
            myMsg = 'ready';
            connected = true;
            myStatus = 2;

			// initialize the led stripe
            window.socket.send("init")
            
            // give the connection some time to establish. Do this by waiting one
            // second. After that, call the callback function so Scratchx knows we're
            // done initializing the connection.
            window.setTimeout(function() {
            	callback();
            }, 1000);

        };

        window.socket.onmessage = function (message) {
        	// We're not expecting anything back from the websocket (yet)
            var msg = message.data;
            console.log(message.data)
        };

        window.socket.onclose = function (e) {
            console.log("Connection closed.");
            socket = null;
            connected = false;
            myMsg = 'not_ready';				// back to yellow status.
            myStatus = 1;
        };
    };

    // Cleanup function when the extension is unloaded
    ext._shutdown = function () {
        var msg = "clear";
        window.socket.send(msg);
        window.socket.onclose = function () {}; // disable onclose handler first
    	window.socket.close();					// close the socket.
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function (status, msg) {
        return {status: myStatus, msg: myMsg};
    };

    // when the connect to server block is executed
    ext.clearPixels = function () {
        if (connected == false) {
            alert("Server Not Connected");
        }
        window.socket.send("clear");
    };
    
    ext.setPixels = function (red, green,blue) {
    	var msg = "setpixels " + String(red) + " " + String(green) + " " + String(blue);
    	window.socket.send(msg);
    };
    
    ext.setPixel = function (pixel, red, green, blue) {
    	var msg = "setpixel " + String(pixel) + " " + String(red) + " " + String(green) + " " + String(blue);
    	window.socket.send(msg);
    };
    
    ext.autoShow = function (autoShowValue) {
    	if (autoShowValue == "On") {
    		window.socket.send("autoshow on");
    	} else {
    		window.socket.send("autoshow off");
    	}
    };
    
    ext.show = function () {
    	window.socket.send("show");
    };
    
    ext.shiftPixels = function (direction) {
    	if (direction == "Left") {
    		window.socket.send("shift left");
    	} else {
    		window.socket.send("shift right");
    	}
    };
    
    ext.dim = function (dimAmount) {
      var msg = "dim " + String(dimAmount);
      window.socket.send(msg);
    };
    
    ext.discnct = function () {
        var msg = "clear";
        window.socket.send(msg);
        window.socket.onclose = function () {}; // disable onclose handler first
    	window.socket.close();					// close the socket.    	
    	socket = null;
        connected = false;
        myMsg = 'not_ready';				// back to yellow status.
        myStatus = 1;
    };

    // Block and block menu descriptions
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
            [" ", 'Dim pixels %n', 'dim', "1"]
            //[" ", "Set BCM %n Output to %m.high_low", "digital_write", "PIN", "0"],
            //[" ", "Set BCM PWM Out %n to %n", "analog_write", "PIN", "VAL"],
            //[" ", "Tone: BCM %n HZ: %n", "play_tone", "PIN", 1000],
            //["r", "Read Digital Pin %n", "digital_read", "PIN"]

        ],
        "menus": {
            "direction": ["Left", "Right"],
            "showstate": ["On", "Off"]

        },
        url: 'https://github.com/ronbuist/ws2801scratch'
    };

    // Register the extension
    ScratchExtensions.register('ws2801', descriptor, ext);
})({});
