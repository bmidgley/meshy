# meshy

Using a raspberry pi 2 with TL-wn722n adapter and a grovepi kit for the display. Software is hsmm-pi.

If a buzzer is connected to D8, you will hear a beep that is longer for higher signal quality so you
can "hear" how good the signal is. I plan to be able to switch that to a different port to get broadcast
alerts from the mesh.

Run meshy.py on boot and it will scan for and log contact with mesh networks. It will also try to resolve
and cache network names (callsigns) for use later. Add a GPS like the GPS-360 and set up hsmm-pi to
broadcast your gps location and the logs will include location data.

![alt tag](https://raw.github.com/bmidgley/meshy/master/images/meshy.png)

