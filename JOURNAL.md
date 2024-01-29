# Design Journal

## 2024-1-7
I've been working with my Sparkfun IMU with great success! I did some reading on SPI and I2C, then I plugged my IMU into my Arduino and everything worked! Right now, I can get my computer to display the accelerometer, gyroscope, magnetometer and thermometer readings through a serial port.

Thinking about how to measure where a point is in space, and I'm thinking about combining the magnetometer and the accelerometer. The benefit of the magnetometer is that if I had a magnet in the middle of my hand, I could (at least in theory) always accurately determine where my finger was relative to the hand. This does face the minor problem of interference from other magnets, which means I'll need to use the accelerometer as well.

I'm  happy with how this is going so far! Until next time.

## 2024-2-28
I worked on some other stuff, but now that I'm mostly done with my Waland tomfoolery I can get back to work on this :) I looked at the Digital Motion Processor on my IMU and it seemed pretty cool, my only problem is that the controller takes up more space than my Arduino can handle lol. I'm going to need a better arduino, hopefully I can also start running it on my main Linux PC instead of my old Mac laptop. There's lots of stuff I'm still thinking about, but I'm pretty much ready to fully get started on this project. Should be fun :D
