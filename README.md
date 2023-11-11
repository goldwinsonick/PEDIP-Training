## This project is for Magang KRAI 2023.

### Created: 17/08/2023

This repo contains a data collection app that records data through a serial port. Data that is collected is used to determine the speed of a shooter motor based on the angle of the shooter and distance of robot.

### Data collected

dist - distance between robot and ring based on LIDAR

rpm - rpm speed of the shooter friction wheel motor

ang - angle of the shooter from vertical (0 degrees) to horizontal (90 degrees)

success - 1(Ball goes in the ring), 0.5(Almost), 0(Ball doesn't go in the ring)

### Data Analysis
With parameter dist and ang, a model should return the rpm of the motor. We use polynomial regression of the data.