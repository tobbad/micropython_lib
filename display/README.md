# Display #

Code in this folder supports different kind of displays.

## Led matrix code ##
I obtained a 32x32 RGB Led matrix display from here:
http://www.play-zone.ch/de/bauteile/led/segmente-matrix/rgb-led-panel-32x32.html
they reference following page for the wire up of this display:
https://learn.sparkfun.com/tutorials/rgb-panel-hookup-guide
This kind of panels is reversed engineered for example here:
http://www.rayslogic.com/propeller/Programming/AdafruitRGB/AdafruitRGB.htm

When I build my STM32F4Disco shield I added a connector to drive the input of this device.

Basically you have 6 x 32 bit shift register with the data input connected to 'R0', 'R1', 'G0', 'G1', 'B0' and 'B1'. These shift registers are realized with a chip similar to [MPI5026](http:/www.rayslogic.com/propeller/Programming/AdafruitRGB/MBI5026.pdf). The data is shifted into the register with the rising edge of 'clk'. This chip can directly drive the cathode of a led. The output of the shift register is connected to a output latch controlled by the 'stb', 'strobe' or 'latch' signal. If this input is set to `H` the shift register output is the output of the latch register. If you set the `latch` control signal to `L` the latch register output stays fixed at the input just before the latch signal edge. To drive the MBI5026 output there is further an output enable `oe` which drives the cathode of the LED with a constant current difined by the chips `R-EXT` input. By daisy chain several such chips you can build larger displays.
<p align="center">
  <img src="pic/MBI5026.png" alt="Block diagramm of MBI5026"/>
</p>

The annode is connected over a 3:8 demultiplexer (eg [74HC138](http://www.mouser.com/ds/2/405/sn74hc138-445126.pdf)) to 'a', 'b' if you own a 32x16 Led matrix. If you do have the 'd' connector you have a 4:16 demultiplexer and therfore a 32x32 display. As this chip can not drive the necessary current for 64 LEDs there are switching elements on the panel to do that.

