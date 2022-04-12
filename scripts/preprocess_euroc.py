import csv
import sys
import yaml

if len(sys.argv) < 2:
    print("unspecified dataset")
    sys.exit()

prefix = sys.argv[1]

# path = '/media/duyanwei/du/data/Euroc/MAV/MH_05_difficult/mav0/cam0/'

# times.txt
file = prefix + '/data.csv'
output = open(prefix + '/times.txt', 'w')

with open(file) as csvfile:
    f = csv.reader(csvfile)
    next(f)
    for row in f:
        output.write(row[0] + ' ' + str(float(row[0]) / 1e9) + '\n')
output.close()

# camera.txt (intrinsic)
file = prefix + '/sensor.yaml'
output = open(prefix + '/camera.txt', 'w')
with open(file) as yamlfile:
    # read
    sensor = yaml.load(yamlfile, Loader=yaml.FullLoader)
    S = sensor["resolution"]
    K = sensor["intrinsics"]
    D = sensor["distortion_coefficients"]

    # start to write
    output.write("RadTan ")
    output.write(str(K[0] / S[0]) + " " + str(K[1] / S[1]) + " " + str(K[2] / S[0]) + " " + str(K[3] / S[1]) + " ")
    output.write(str(D[0]) + " " + str(D[1]) + " " + str(D[2]) + " " + str(D[3]) + "\n")
    output.write(str(S[0]) + " " +str(S[1]) + "\n")
    output.write("crop\n")
    output.write(str(S[0]) + " " +str(S[1]))
output.close()