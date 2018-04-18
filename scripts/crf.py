"""
Adapted from the inference.py to demonstate the usage of the util functions.
"""

import sys
import numpy as np
from math import pi, sqrt, exp
import pydensecrf.densecrf as dcrf
from flowlib import read_flow, write_flow

# Get im{read,write} from somewhere.
try:
    from cv2 import imread, imwrite
except ImportError:
    # Note that, sadly, skimage unconditionally import scipy and matplotlib,
    # so you'll need them if you don't have OpenCV. But you probably have them.
    from skimage.io import imread, imsave
    imwrite = imsave
    # TODO: Use scipy instead.

from pydensecrf.utils import unary_from_labels, create_pairwise_bilateral, create_pairwise_gaussian
def gaussian(n, sigma=2):
    r = range(-int(n / 2), int(n / 2) + 1)
    return [1 / (sigma * sqrt(2 * pi)) * exp(-float(x) ** 2 / (2 * sigma ** 2)) for x in r]

def getUnaryPotentialFromFlows(flow, flow_range):
    n = 2 * flow_range + 1
    gauss_kernel = gaussian(n)

    flow_flat = flow.flatten()
    U = np.zeros((flow_range, flow_flat.shape[0]))
    for i, pixel_flow in enumerate(flow_flat):
        # Center the Gaussian filter at the predicted flow value for the current pixel:
        left_index = flow_range - pixel_flow + 1
        col = np.copy(gauss_kernel[left_index:left_index + flow_range])
        U[:, i] = col
        #col = col / col.sum() # Normalize so probabilities sum to 1
        #U[:, i] = -np.log(col)
    U = U/U.sum(axis=0,keepdims=1)
    U = -np.log(U)
    return U.astype(np.float32)

if len(sys.argv) != 4:
    print("Usage: python {} IMAGE_0 FLO_FILE OUTPUT_FLO_FILE".format(sys.argv[0]))
    print("")
    print("IMAGE_0 is the first input image.")
    print("FLO_FILE is the flow predictions generated by the FlowNet.")
    print("OUTPUT_FLO_FILE is the output file where the updated flow should be written.")
    sys.exit(1)

fn_im = sys.argv[1]
fn_flo = sys.argv[2]
fn_output = sys.argv[3]

#################################
### Read input image and flow ###
#################################
img_rgb = imread(fn_im)

flow_xy = read_flow(fn_flo)
flow_xy = np.rint(flow_xy) # Round flows to nearest integer
flow_xy = flow_xy.astype(int)
print("flow[0][0]: " + str(flow_xy[0][0]))
print("flow[25][25]: " + str(flow_xy[25][25]))
print("flow[100][100]: " + str(flow_xy[100][100]))

flow_xy_out = np.empty_like(flow_xy)

for axis in range(2):
    if axis == 0:
        print("Processing x flows:")
    else:
        print("Processing y flows:")
    flow = flow_xy[:, :, axis]
    min_flow = np.amin(flow)
    max_flow = np.amax(flow)

    shift = 1 - min_flow
    flow_range = max_flow + shift
    flow = flow + shift # Shift flows to all be positive integers
    print("The minimum flow is: " + str(min_flow))
    print("The maximum flow is: " + str(max_flow))

    ###########################
    ### Setup the CRF model ###
    ###########################
    d = dcrf.DenseCRF(flow.shape[1] * flow.shape[0], flow_range)

    # Get Unary Potential (Negative Log Likelihood of each possible flow value at
    # every pixel location)
    U = getUnaryPotentialFromFlows(flow, flow_range)
    d.setUnaryEnergy(U)

    # Create compatibility matrix. This matrix provides a measure of
    # compatibility between flow measurements. (Similar flows should have a
    # lower pairwise energy)
    compat_matrix = np.zeros((flow_range, flow_range), dtype=np.float32)
    for i in range(flow_range):
        for j in range(flow_range):
            compat_matrix[i][j] = np.abs(i - j)

    # Create the proximity-based energy.
    # These features do not depend on the image colours, and they encourage
    # nearby pixels to have similar flows:
    feats = create_pairwise_gaussian(sdims=(3, 3), shape=flow.shape[:2])
    d.addPairwiseEnergy(feats,
                        compat=compat_matrix,
                        kernel=dcrf.DIAG_KERNEL,
                        normalization=dcrf.NORMALIZE_SYMMETRIC)

    # Create the colour-dependent energy.
    # These features encourage nearby pixels with similar colours to have similar
    # flows more than pixels with different colours:
    feats = create_pairwise_bilateral(  sdims=(80, 80),
                                        schan=(13, 13, 13),
                                        img=img_rgb,
                                        chdim=2)
    d.addPairwiseEnergy(feats,
                        compat=compat_matrix,
                        kernel=dcrf.DIAG_KERNEL,
                        normalization=dcrf.NORMALIZE_SYMMETRIC)


    ####################################
    ### Do inference and compute MAP ###
    ####################################

    # Run five inference steps.
    Q = d.inference(5)

    # Find out the most probable class for each pixel.
    MAP = np.argmax(Q, axis=0)
    MAP = MAP - shift
    flow_xy_out[:, :, axis] = MAP.reshape(flow.shape)

print("flow[0][0]: " + str(flow_xy_out[0][0]))
print("flow[25][25]: " + str(flow_xy_out[25][25]))
print("flow[100][100]: " + str(flow_xy_out[100][100]))
# Write to output file:
write_flow(fn_output, flow_xy_out)
'''
# Just randomly manually run inference iterations
Q, tmp1, tmp2 = d.startInference()
for i in range(5):
    print("KL-divergence at {}: {}".format(i, d.klDivergence(Q)))
    d.stepInference(Q, tmp1, tmp2)
'''