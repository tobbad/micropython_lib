TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
cp ${ROOT}/lib/*.py ${TARGET}
cp *.py ${TARGET}
cp ${ROOT}/display/led_matrix_accel.py ${TARGET}
cp ${ROOT}/applications/tetris.py ${TARGET}
