from __future__ import print_function
from flowlib import evaluate_flow, read_flow, write_flow
from crf import apply_crf
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

for ent in ops:
    fn_img = ent[0]
    fn_flo = ent[3]
    fn_out = fn_flo[:fn_flo.rindex('.')] + '_crf.flo'
    crf_flo = apply_crf(fn_img, fn_flo)
    write_flow(fn_out, crf_flo)
    print("Wrote to: " + fn_out)
