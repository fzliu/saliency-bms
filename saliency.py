"""
saliency.py - An implementation of Zhang and Sclaroff's Boolean Map Saliency
algorithm. http://cs-people.bu.edu/jmzhang/BMS/BMS_iccv13_preprint.pdf.

author: Frank Liu - frank.zijie@gmail.com
last modified: 04/19/2016

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Frank Liu (fzliu) nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Frank Liu (fzliu) BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# system imports
import argparse
import os
import timeit

# library imports
import cv2
import numpy as np
from skimage.color import gray2rgb, rgb2lab
from skimage.io import imread, imsave
from skimage.transform import rescale

N_THRESHOLDS = 10
MAX_DIM = 320

parser = argparse.ArgumentParser(description="Compute a saliency map.",
                                 usage="saliency.py -i <input_path>")
parser.add_argument("-i", "--input", type=str, required=True, help="input path")


def activate_boolean_map(bool_map):
    """
        Performs activation on a single boolean map.
    """

    # use the boolean map as a mask for flood filling
    activation = np.array(bool_map, dtype=np.uint8)
    mask_shape = (bool_map.shape[0] + 2, bool_map.shape[1] + 2)
    ffill_mask = np.zeros(mask_shape, dtype=np.uint8)

    # top and bottom rows
    for i in range(0, activation.shape[0]):
        for j in [0, activation.shape[1] - 1]:
            if activation[i,j]:
                cv2.floodFill(activation, ffill_mask, (j, i), 0)

    # left and right columns
    for i in [0, activation.shape[0] - 1]:
        for j in range(0, activation.shape[1]):
            if activation[i,j]:
                cv2.floodFill(activation, ffill_mask, (j, i), 0)

    return activation

def compute_saliency(img):
    """
        Computes Boolean Map Saliency (BMS).
    """

    img_lab = rgb2lab(img)/255
    thresholds = np.arange(img_lab.min(), img_lab.max(), 1.0 / N_THRESHOLDS)[1:]

    # compute boolean maps
    bool_maps = []
    for thresh in thresholds:
        img_lab_T = img_lab.transpose(2, 0, 1)
        img_thresh = (img_lab_T > thresh)
        bool_maps.extend(list(img_thresh))

    # compute mean attention map
    attn_map = np.zeros(img_lab.shape[:2], dtype=np.float)
    for bool_map in bool_maps:
        attn_map += activate_boolean_map(bool_map)
    attn_map /= N_THRESHOLDS

    # gaussian smoothing
    attn_map = cv2.GaussianBlur(attn_map, (0, 0), 3)

    # perform normalization
    norm = np.sqrt((attn_map**2).sum())
    attn_map /= norm
    attn_map /= attn_map.max() / 255

    return attn_map.astype(np.uint8)

def main(args):
    """
        Entry point.
    """

    # load the image
    img = imread(args.input)
    if img.ndim == 2:
        img = gray2rgb(img)
    elif img.shape[2] == 4:
        img = img[:, :, :3]
    upper_dim = max(img.shape[:2])
    if upper_dim > MAX_DIM:
        img = rescale(img, MAX_DIM/float(upper_dim), order=3) 

    # compute saliency
    start = timeit.default_timer()
    img_sal = compute_saliency(img)
    runtime = timeit.default_timer() - start
    print("Took {0} seconds.".format(runtime))

    # save image
    (fname, ext) = os.path.splitext(args.input)
    out_path = fname + "_saliency" + ext
    imsave(out_path, img_sal)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
