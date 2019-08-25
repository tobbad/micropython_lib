TARGET=/media/badi/PYBFLASH
ROOT=../../
rm -rf ${TARGET}/*

TRGT=1

cp ${ROOT}/display/led36.py ${TARGET}
#cp board.py ${TARGET}
if [ $TRGT == 1 ]
then
    cp main.py sensa.py ${TARGET}
elif [ $TRGT == 2 ]
then
    cp -r www ${TARGET}
    cp main_www.py  ${TARGET}/main.py
    cp microWeb*.py ${TARGET}
elif [ $TRGT == 3 ]
then
    echo "Not defined"
fi


