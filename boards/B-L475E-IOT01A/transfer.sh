#TARGET=/media/badi/5C5A-C65E/
TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
cp ${ROOT}/lib/*.py ${TARGET}
cp board.py ${TARGET}
cp main.py ${TARGET}main.py
cp ${ROOT}/sensor/hts221*.py ${TARGET}
