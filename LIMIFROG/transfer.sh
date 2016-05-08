TARGET=/media/badi/PYBFLASH/
rm ${TARGET}/*
cp ../lib/* ${TARGET}
cp main.py ${TARGET}
cp board.py ${TARGET}
cp ../lis3mdl_const.py ${TARGET}
cp ../lis3mdl.py ${TARGET}
cp ../lps25h* ${TARGET}
cp ../lsm6ds3* ${TARGET}
cp ../vl6180x* ${TARGET}