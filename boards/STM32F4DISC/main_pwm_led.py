#!/usr/bin/env python
#
# Main file for STM32F4DISCOVERY
#
from board import config
import pyb
import math

periode_us=1000
tim_nr = config['led']['tim_ch'][0][0]
t = pyb.Timer(tim_nr, prescaler=168, period=periode_us)
tch=()
for pin, (tim,ch) in zip(config['led']['pins'], config['led']['tim_ch']):
    tch += (t.channel(ch, pyb.Timer.PWM, pin=pyb.Pin(pin)),)

wait_tick=5
dphi=5/180*math.pi
Dphi=90/180*math.pi
idx=0

while True:
    phi = idx*dphi
    for i, ch in enumerate(tch):
        pwm_value = int(periode_us/2*(1+math.sin(phi+i*Dphi)))
        ch.pulse_width(pwm_value)
    pyb.delay(wait_tick)
    idx+=1

