from __future__ import print_function
from flowlib import evaluate_flow, read_flow
import os, sys, numpy as np
import argparse
from scipy import misc
import caffe
import tempfile
from math import ceil

parser = argparse.ArgumentParser()
parser.add_argument('listfile', help='one line should contain paths "img0.ext img1.ext gt.flo out.flo"')

args = parser.parse_args()

if(not os.path.exists(args.listfile)): raise BaseException('listfile does not exist: '+args.listfile)

def readTupleList(filename):
    list = []
    for line in open(filename).readlines():
        if line.strip() != '':
            list.append(line.split())

    return list

ops = readTupleList(args.listfile)

width = -1
height = -1
total_epe = 0
count = 0
for ent in ops:

    # Calculate End-Point Error
    gt_flow = read_flow(ent[2])
    pred_flow = read_flow(ent[3])
    epe = evaluate_flow(gt_flow, pred_flow)
    print("EPE: " + str(epe))
    total_epe += epe
    count += 1
mean_epe = total_epe / count
print("Mean epe: " + str(mean_epe))
