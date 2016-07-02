TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
cp ${ROOT}/lib/*.py ${TARGET}
cp *.py ${TARGET}
cp ${ROOT}/display/led_matrix_accel.py ${TARGET}
cp ${ROOT}/display/led_matrix_server.py ${TARGET}
cp ${ROOT}/applications/tetris.py ${TARGET}
cp ${ROOT}/applications/conway.py ${TARGET}
cp ${ROOT}/micropyGPS/micropyGPS.py ${TARGET}
