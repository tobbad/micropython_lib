TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
cp ${ROOT}/lib/* ${TARGET}
cp *.py ${TARGET}
cp ${ROOT}/sensor/lis3xxx* ${TARGET}
cp ${ROOT}/sound/cs43l22* ${TARGET}