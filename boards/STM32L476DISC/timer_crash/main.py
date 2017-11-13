# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:33:56 2017

@author: z003tauu
"""
from board import config
from pyb import Pin, ExtInt, Timer
from oneshot import OneShot

# Is connected to Time 1 channel 2 (TIM2_CH2)
left_sw = Pin(config['switch']['pins'][1], 
                  mode=config['switch']['conf'][1][0],
                  pull=config['switch']['conf'][1][1])
# Led is connected to (TIM1_CH1N)
led_g = Pin(config['led']['pins'][1], mode=Pin.OUT_PP)

timer_number=1
timer_channel=2
oneshot = OneShot(led_g, timer_number, timer_channel)
oneshot.pulse_us(500)
oneshot.pause_us(500000)
oneshot.trigger_pin(left_sw)
