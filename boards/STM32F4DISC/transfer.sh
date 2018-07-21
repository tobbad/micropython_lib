TARGET=/media/badi/PYBFLASH
ROOT=../../
rm -rf ${TARGET}/*

TRGT=3

cp ${ROOT}/lib/[i-m]*.py ${TARGET}
cp board.py ${TARGET}
#cp main_lps22.py ${TARGET}/main.py
#cp  ${ROOT}/sensor/lps22* ${TARGET}
#cp  ${ROOT}/sound/cs43l22.py ${TARGET}
#cp ${ROOT}/display/led_matrix_accel.py ${TARGET}
#cp ${ROOT}/display/led_matrix_server.py ${TARGET}
#cp ${ROOT}/applications/tetris.py ${TARGET}
#cp ${ROOT}/applications/conway.py ${TARGET}
#cp ${ROOT}/micropyGPS/micropyGPS.py ${TARGET}
if [ $TRGT == 1 ]
then
    cp ${ROOT}/common/datalink.py  ${TARGET}
    cp main_com_test.py ${TARGET}/main.py
elif [ $TRGT == 2 ]
then
    cp main_pwm_led.py ${TARGET}/main.py
elif [ $TRGT == 3 ]
then
    cp ${ROOT}/shields/dragino_LoRa_1_3.py ${TARGET}/
    cp ${ROOT}/rf/sx127x_const.py ${TARGET}/
    cp ${ROOT}/rf/sx127x.py ${TARGET}/
    cp main_lora.py ${TARGET}/main.py
fi


