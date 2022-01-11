# Objects detection algotitms

The algortim based on OpenMV H7+ cam, though camera we can:

- Meansure distance for object in real time
- Corelation with robot frame
- Control light 
- Send data to robot via sockets

## Features

- Angle correction based on blob center and major line ends
- Image masking in not reachable robot position
- Colision detection with another element (picking objects apart of elements which can do collision with robot gripper)

If robot receive flag, camera send via olimex list of available to pick elements

## Visualization of an anti-collision system with a robot gripper:
<p align="center">
<img style="border: 10px solid white;" src="https://raw.githubusercontent.com/openmv/openmv-media/master/boards/openmv-cam/v3/web-new-cam-v3-angle.jpg" width="320" height="320">
</p>
