import sys
import zipfile
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import os
import json
import glob
import cv2

def plot_histogram():
    directory = sys.argv[1]
    files = glob.glob(directory + '/*.txt')
    for file in files:
        with open(file) as f:
            deg = []
            data = np.loadtxt(f)
            for m in data:
                gradient = m[3:5]
                flow = m[5:7]
                inner = np.inner(gradient, flow)
                norms = np.linalg.norm(gradient) * np.linalg.norm(flow)
                if norms < 1e-3:
                    continue
                cos = inner / norms
                rad = np.arccos(np.clip(cos, -1.0, 1.0))
                deg.append(np.rad2deg(rad))
            # make a histogram plot
            plt.title('histogram of the angle between the flow and the gradient directions')
            plt.hist(deg, bins=20)
            plt.xlabel('angle (degree)')
            plt.ylabel('number')
            filename, extname = os.path.splitext(os.path.basename(file))
            plt.savefig(directory + "/hist/" + filename + ".png")
            # plt.show()
            plt.close()

def generate_gf_ratio():
    # get directory
    directory = sys.argv[1]

    # read error file from zip dir and record each row as [timestamp, error]
    error = []
    timestamps = []
    with open(directory + '/results_10.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"] / 10 / 0.05
        timestamps = data["timestamps.npz"]

    # read frame tracking stats and record each row as [timestamp, feature_num, good_feature_num, residual]
    fstats = []
    with open(directory + '/stats_frame_tracking.txt', 'r') as f:
        for line in f:
            data = [float(x) for x in line.split()]
            fstats.append(data[-5:-1])
    '''
    for each piece of data in frame tracking stats, find a match in error stats and record each rows as 
    [timestamp, error, ratio = good_feature_num / feature_num, residual], 
    '''
    data = []
    for v in fstats:
        for i in range(len(timestamps)):
            if v[0] == timestamps[i]:
                if v[2] == 0:
                    continue
                data.append([v[0], error[i], v[2] / v[1], v[3]])
                break
    print(len(data))
    data_array = np.array(data)

    # plot the data
    plt.title('GF ratio V.S. RPE')
    plt.xlabel('RPE (m/s)')
    plt.ylabel('GF ratio')
    plt.plot(data_array[:, 1], data_array[:, 2], 'b.')
    # plt.plot(timestamps, error, 'b.')
    plt.savefig(directory + "/GFRatio_RPE.png")
    plt.show()
    plt.close()

def generate_table():
    directory = sys.argv[1]
    fname1 = 'stats_system.txt'
    fname2 = 'results.zip'
    for root, dirs, files in os.walk(directory):
        if fname1 not in files:
            continue
        rmse = 0
        kf_num = 0
        f_num = 0
        with open(os.path.join(root, fname1), 'r') as f:
            for line in f:
                data = [int(x) for x in line.split()]
                kf_num = data[1]
                f_num = data[2]
        with open(os.path.join(root, fname2)) as f:
            data = np.load(f)
            rmse = json.loads(data['stats.json'])['rmse']
        print(root + ':\n {:.2f} / {} / {}'.format(rmse, kf_num, f_num))


def plot_rpe():
    # get directory
    directory = sys.argv[1]

    # figure
    plt.title('RPE (seconds)')
    plt.xlabel('timestamp (second)')
    plt.ylabel('RPE (m/s)')

    # read error file from zip dir and record each row as [timestamp, error]
    error1 = []
    timestamp1 = []
    with open(directory + '/results_1.zip') as f:
        data = np.load(f)
        error1 = data["error_array.npz"]
        timestamp1 = data["timestamps.npz"]
    error1_array = np.array(error1) / 0.05
    timestamp1_array = np.array(timestamp1)
    plt.plot(timestamp1_array, error1_array, 'r')

    error = []
    timestamp = []
    with open(directory + '/results_10.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"]
        timestamp = data["timestamps.npz"]
    error_array = np.array(error) / 10 / 0.05
    timestamp_array = np.array(timestamp)
    print len(timestamp)
    plt.plot(timestamp_array, error_array, 'g')

    error = []
    timestamp = []
    with open(directory + '/results_50.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"]
        timestamp = data["timestamps.npz"]
    error_array = np.array(error) / 50 / 0.05
    timestamp_array = np.array(timestamp)
    print len(timestamp)
    plt.plot(timestamp_array, error_array, 'b')

    error = []
    timestamp = []
    with open(directory + '/results_100.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"]
        timestamp = data["timestamps.npz"]
    print len(timestamp)
    error_array = np.array(error) / 100 / 0.05
    timestamp_array = np.array(timestamp)
    plt.plot(timestamp_array, error_array, 'y')
    plt.legend(['0.05s', '0.5s', '2.5s', '5s'])

    plt.savefig(directory + "/rpe_second.png")
    plt.show()
    plt.close()

def plot_rpe_m():
    # get directory
    directory = sys.argv[1]

    # figure
    plt.title('RPE (meters)')
    plt.xlabel('timestamp (second)')
    plt.ylabel('RPE (m/m)')

    # read error file from zip dir and record each row as [timestamp, error]
    error = []
    timestamp = []
    with open(directory + '/results_01_m.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"]
        timestamp = data["timestamps.npz"]
    error_array = np.array(error) / 0.1
    timestamp_array = np.array(timestamp)
    plt.plot(timestamp_array, error_array, 'r')

    error = []
    timestamp = []
    with open(directory + '/results_1_m.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"]
        timestamp = data["timestamps.npz"]
    error_array = np.array(error)
    timestamp_array = np.array(timestamp)
    print len(timestamp)
    plt.plot(timestamp_array, error_array, 'g')

    error = []
    timestamp = []
    with open(directory + '/results_5_m.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"]
        timestamp = data["timestamps.npz"]
    error_array = np.array(error) / 5
    timestamp_array = np.array(timestamp)
    print len(timestamp)
    plt.plot(timestamp_array, error_array, 'b')

    error = []
    timestamp = []
    with open(directory + '/results_10_m.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"]
        timestamp = data["timestamps.npz"]
    print len(timestamp)
    error_array = np.array(error) / 10
    timestamp_array = np.array(timestamp)
    plt.plot(timestamp_array, error_array, 'y')
    plt.legend(['0.1m', '1m', '5m', '10m'])

    plt.savefig(directory + "/rpe_meter.png")
    plt.show()
    plt.close()


def generate_result():
    # get directory
    directory = sys.argv[1]

    # read error file from zip dir and record each row as [timestamp, error]
    error = []
    timestamps = []
    with open(directory + '/results.zip') as f:
        data = np.load(f)
        error = data["error_array.npz"] / 10 / 0.05
        timestamps = data["timestamps.npz"]

    # read frame tracking stats and record each row as [timestamp, feature_num, good_feature_num, residual]
    fstats = [] # [timestamp, id]
    with open(directory + '/stats_frame_tracking.txt', 'r') as f:
        for line in f:
            data = [float(x) for x in line.split()]
            fstats.append([data[-5], data[1]])
    '''
    for each piece of data in frame tracking stats, find a match in error stats and record each rows as 
    [error, id], 
    '''
    data = []
    for v in fstats:
        for i in range(len(timestamps)):
            if v[0] == timestamps[i]:
                data.append([error[i], v[1]])
                break

    data.sort(key=lambda x: x[0])

    for i in range(500, len(data) / 2, 10):
        j = len(data) - i - 1
        flow_im = mpimg.imread(directory + "../flow/" + str(int(data[i][1])) + ".jpg")
        hist_im = mpimg.imread(directory + "../flow/hist/" + str(int(data[i][1])) + ".png")
        
        flow_im2 = mpimg.imread(directory + "../flow/" + str(int(data[j][1])) + ".jpg")
        hist_im2 = mpimg.imread(directory + "../flow/hist/" + str(int(data[j][1])) + ".png")

        twist = []
        with open(directory + "../flow/twist/" + str(int(data[j][1])) + "_twist.txt") as f:
            twist = np.loadtxt(f)

        plt.figure("Green: selected features")

        plt.subplot(2, 2, 1)
        plt.imshow(flow_im)
        plt.xlabel('RPE error = ' + str(format(data[i][0], '.4f')) + 'm/s')
        plt.subplot(2, 2, 3)
        plt.imshow(hist_im)
        plt.xlabel('v = ' + str(twist[0]) + ', ' + str(twist[1]) + ', ' + str(twist[2]))
    
        plt.subplot(2, 2, 2)
        plt.imshow(flow_im2)
        plt.xlabel('RPE error = ' + str(format(data[j][0], '.4f')) + 'm/s')
        plt.subplot(2, 2, 4)
        plt.imshow(hist_im2)
        #plt.savefig(directory + "../result/" + str(i) + ".png", dpi=500)
        plt.show()
        plt.close()

if __name__ == '__main__':
    print('hello world')
    generate_result()
    # plot_histogram()