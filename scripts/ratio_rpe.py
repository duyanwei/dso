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
