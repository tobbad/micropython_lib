TARGET=/media/badi/PYBFLASH/
ROOT=../../

CONF=2

rm ${TARGET}/*
cp ${ROOT}/lib/* ${TARGET}
cp main.py board.py ${TARGET}
if [ $CONF == 0 ] || [ $CONF == 1 ]
then
    cp ${ROOT}/sensor/lsm303c* ${TARGET}
    cp ${ROOT}/sensor/l3gd20* ${TARGET}
    cp ${ROOT}/sensor/mfx* ${TARGET}
elif [ $CONF == 2 ]
then
    cp ${ROOT}/test/uart_idle.py ${TARGET}
elif [ $CONF == 3 ]
then
    cp ${ROOT}/3d/mgc3x30.py ${TARGET}
fi

echo "conf=$CONF" > ${TARGET}/conf.py

         
