#!/bin/shh

reset

DIR="/media/duyanwei/du/data/Euroc/MAV/"
POOL=$(ls $DIR | grep .zip)

for ELEMENT in $POOL
do
    DATASET=${ELEMENT%.*}
  
    # if [ -d $DATASET ];then
    #     continue
    # fi
  
    echo  "" # empty line
    echo "Processing "$DATASET

    DIRECTORY="/media/duyanwei/du/data/Euroc/MAV/$DATASET"
    PREFIX=$DIRECTORY"/mav0/cam0"

    #------------------------- preprocess data ----------------------------------
    echo "-------- Preprocess data ---------"
    # unzip data
    if [ ! -d $PREFIX ]; then
        echo "unzip ..."
        echo ${DIRECTORY}
        unzip -qo ${DIRECTORY}.zip -d $DIRECTORY
    fi

    # prepare camera intrinsic file and timestamps
    if [ ! -f $PREFIX/camera.txt ] || [ ! -f $PREFIX/times.txt ]; then
        python ../scripts/preprocess_euroc.py $PREFIX
    fi

    # prepare ground truth
    if [ ! -f $PREFIX/data.tum ]; then
        evo_traj euroc $PREFIX/../state_groundtruth_estimate0/data.csv --save_as_tum
        mv data.tum $PREFIX
    fi

    #------------------------- launch program ----------------------------------
    sh ../scripts/run_EuRoC.sh $PREFIX

    #------------------------- Evaluation ----------------------------------
    sleep 2
    echo "--------Evaluation---------"
    mkdir $DATASET
    mv stats_*.txt $DATASET
    evo_rpe tum $PREFIX/data.tum $DATASET/stats_tracking_result.txt -va --correct_scale --align --save_results $DATASET/results.zip -u f -d 10 --all_pairs
    echo "----------Done-------------"
    echo "" # empty line
    exit
done