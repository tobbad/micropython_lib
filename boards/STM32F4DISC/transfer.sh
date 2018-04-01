TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
#cp ${ROOT}/lib/*.py ${TARGET}
cp board.py ${TARGET}
#cp main_lps22.py ${TARGET}/main.py
#cp  ${ROOT}/sensor/lps22* ${TARGET}
#cp  ${ROOT}/sound/cs43l22.py ${TARGET}
#cp ${ROOT}/display/led_matrix_accel.py ${TARGET}
#cp ${ROOT}/display/led_matrix_server.py ${TARGET}
#cp ${ROOT}/applications/tetris.py ${TARGET}
#cp ${ROOT}/applications/conway.py ${TARGET}
#cp ${ROOT}/micropyGPS/micropyGPS.py ${TARGET}
cp ${ROOT}/common/datalink.py  ${TARGET}
cp main_com_test.py ${TARGET}/main.py
