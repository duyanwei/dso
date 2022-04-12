# EVO
## Install
- https://blog.csdn.net/qq_37568167/article/details/105594262

- git clone https://github.com/MichaelGrupp/evo.git
- cd evo
- pip install -i https://pypi.tuna.tsinghua.edu.cn/simple evo --upgrade --no-binary evo


# EUROC
- gt: /state_groundtruth_estimate0/data.csv
- evo_traj euroc data.csv --save_as_tum
- evo_traj  tum    CameraTrajectory.txt  --ref=data.tum   -p   --plot_mode=xy  --align  --correct_scale
- evo_ape  tum     data.tum   CameraTrajectory.txt  -va   -p   --plot_mode=xyz
 
