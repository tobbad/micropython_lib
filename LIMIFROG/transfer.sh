#
# Choose what you'd like to deploy on the 
# device
#
SEL="1"
TARGET=/media/badi/PYBFLASH/
rm ${TARGET}/*
cp ../lib/* ${TARGET}
if [ "x$SEL" == "x1" ]
then
    # Show how to read each sensor
    cp main1.py ${TARGET}/main.py
    cp board.py ${TARGET}
    cp ../lis3mdl_const.py ${TARGET}
    cp ../lis3mdl.py ${TARGET}
    cp ../lps25h* ${TARGET}
    cp ../vl6180x* ${TARGET}
    cp ../lsm6ds3* ${TARGET}
fi
if  [ "x$SEL" == "x2" ]
then
    # Simple script showing
    # the usage of the OLED display
    cp main2.py ${TARGET}/main.py
    cp board.py ${TARGET}
    cp demos.py ${TARGET}
    cp ../lsm6ds3* ${TARGET}
    cp ../seps525* ${TARGET}
fi
