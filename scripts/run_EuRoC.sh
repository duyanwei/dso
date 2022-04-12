#!/bin/shh
echo "-------- Run Program ---------"

PREFIX="$1"

# PREFIX="/media/duyanwei/du/data/Euroc/MAV/MH_01_easy/mav0/cam0"

make -j4 &&

bin/dso_dataset \
    files=${PREFIX}/data \
    calib=${PREFIX}/camera.txt \
    preset=0 \
    speed=0.2 \
    mode=1 \
    nolog=1 \
    quiet=1 \
    nogui=1 \
    pointdensity=800 \
    maxFrames=7 \
    kfGlobalWeight=1 \
    reTrackThreshold=2.5 \
    debugGoodFeature=1 \