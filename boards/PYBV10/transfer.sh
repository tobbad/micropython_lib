#TARGET=/media/badi/5C5A-C65E/
TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
cp ${ROOT}/lib/* ${TARGET}
cp main.py ${TARGET}
cp board.py ${TARGET}
cp ${ROOT}/sensor/mma7660* ${TARGET}
cp ${ROOT}/rf/sx127x* ${TARGET}