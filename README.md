# RGB-Room-Lights

This project uses an ESP8266 running a http server to control ws2812b rgb leds. The code in the arduino file is very meshed together and doesn't fit my current programming practices, but it is still something i am very proud of.

RoomLights.ino should have the ssid and password replaced and then flashed into the ESP8266

#Abstract Description
I had some ws2812b led strips, and thought it would be fun to put them up in my room as mood lights. I desgined a controller based around the ESP8266, which ran a web server. This web server took commands that could change the color, run preset modes, like a rainbow, or christmas lights, change the brightness etc.

I then designed a desktop application using python and TKinter to interface with the board to make a clean controller UI 

I also had a google home in my room. I decided that since the chip ran a webserver, I should be able to design a way to control the lights using my google home. The design I came up with is overcomplicated and convoluted, but it used a lot of pre existing tools and fit my use case just fine. Using the free service IFTTT, I set up rules to create a voice command that would take any input after the command and write it to a spreadsheet. Then server.py, which was runing on a linux box 24/7, would check the google sheet for any updates, interpret the command, then issue the appropriate command to the server on the ESP8266. 
