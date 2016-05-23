#TARGET=/media/badi/5C5A-C65E/
LoRa=1
TARGET=/media/badi/PYBFLASH/
ROOT=../../
rm ${TARGET}/*
cp ${ROOT}/lib/*.py ${TARGET}
cp board.py ${TARGET}
cp ${ROOT}/sensor/mma7660* ${TARGET}
cp ${ROOT}/rf/sx127x_* ${TARGET}
if [ "${LoRa}" == "1" ]
then 
    cp ${ROOT}/applications/lora_tx_beacon.py   ${TARGET}main.py
    echo "Copy lora application"
else
    cp main.py ${TARGET}main.py
fi
