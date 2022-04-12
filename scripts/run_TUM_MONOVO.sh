#!/bin/shh

PREFIX="/media/duyanwei/du/data/tum"
SEQ="06"
DIR=${PREFIX}/sequence_${SEQ}

reset && 

make -j4 &&

bin/dso_dataset \
    files=${DIR}/images.zip \
    calib=${DIR}/camera.txt \
    gamma=${DIR}/pcalib.txt \
    vignette=${DIR}/vignette.png \
    preset=0 \
    mode=0 \
    nolog=1 \
    quiet=1 \
    nogui=0 \
    pointdensity=800