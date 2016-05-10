TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
cp ${ROOT}/lib/* ${TARGET}
cp *.py ${TARGET}
cp ${ROOT}/sensor/lsm303c* ${TARGET}
cp ${ROOT}/sensor/l3gd20* ${TARGET}