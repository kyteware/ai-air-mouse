# Design Journal

## 2024-1-7
I've been working with my Sparkfun IMU with great success! I did some reading on SPI and I2C, then I plugged my IMU into my Arduino and everything worked! Right now, I can get my computer to display the accelerometer, gyroscope, magnetometer and thermometer readings through a serial port.

Thinking about how to measure where a point is in space, and I'm thinking about combining the magnetometer and the accelerometer. The benefit of the magnetometer is that if I had a magnet in the middle of my hand, I could (at least in theory) always accurately determine where my finger was relative to the hand. This does face the minor problem of interference from other magnets, which means I'll need to use the accelerometer as well.

I'm  happy with how this is going so far! Until next time.
