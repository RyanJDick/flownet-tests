import sys
import os
import random

video_folder = sys.argv[1]
flo_folder = video_folder[0:video_folder.rindex('/')]
flo_folder = flo_folder[0:flo_folder.rindex('/')] + '/flow/'
occ_folder = video_folder[0:video_folder.rindex('/')]
occ_folder = occ_folder[0:occ_folder.rindex('/')] + '/occlusions/'
#print("Flow folder: " + flo_folder) 

test_list = []
train_list = []
train_test_split = []
for subdir, dirs, files in os.walk(video_folder):
    is_test = random.random() < 0.2
    prev_file_path = None
    files.sort() # Put frames in order
    for file in files:
        file_path = os.path.join(subdir, file)
        if prev_file_path is not None:
            split = prev_file_path.split('/')
            sub_path = split[-2] + '/' + split[-1] 
            #print("1. " + prev_file_path)
            #print("2. " + file_path)
            flo_path = flo_folder + sub_path
            flo_path = flo_path[0:-3] + 'flo'
            #print("3. " + flo_path)
            occ_path = occ_folder + sub_path
            #print("4. " + occ_path)
            result = prev_file_path + '\t' + file_path + '\t' + flo_path + '\t' + occ_path
            if is_test:
                test_list.append(result)
            else:
                is_val = random.random() < 0.15
		if is_val:
                    train_test_split.append(2)
                else:
                    train_test_split.append(1)

                train_list.append(result)    
        prev_file_path = file_path

train_file = open("MPI_Sintel_TRAIN.list", "w")
for line in train_list:
    train_file.write("%s\n" % line)
train_file.close()

test_file = open("MPI_Sintel_TEST.list", "w")
for line in test_list:
    test_file.write("%s\n" % line)
test_file.close()

split_file = open("MPI_Sintel_train_val_split.list", "w")
for line in train_test_split:
    split_file.write("%s\n" % line)
split_file.close()
