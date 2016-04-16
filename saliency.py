"""
saliency.py - An implementation of Zhang and Sclaroff's Boolean Map Saliency
algorithm. http://cs-people.bu.edu/jmzhang/BMS/BMS_iccv13_preprint.pdf.

author: Frank Liu - frank.zijie@gmail.com
last modified: 04/15/2016

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
import numpy as np
from scipy import ndimage
from skimage import img_as_float
from skimage.color import gray2rgb, rgb2lab
from skimage.io import imread, imsave
from skimage.transform import rescale

N_THRESHOLDS = 10
MAX_DIM = 640

parser = argparse.ArgumentParser(description="Compute a saliency map.",
                                 usage="saliency.py -i <input_path>")
parser.add_argument("-i", "--input", type=str, required=True, help="input path")


def compute_saliency(img):
    """
        Computes Boolean Map Saliency (BMS).
    """

    img_lab = rgb2lab(img)/255
    thresholds = np.arange(0, 1, 1.0 / N_THRESHOLDS)[1:]

    # compute boolean maps
    bool_maps = []
    for thresh in thresholds:
        img_lab_T = img_lab.transpose(2, 0, 1)
        bool_maps.extend(list(img_lab_T > thresh))

    # compute mean attention map
    attn_map = np.zeros(img_lab.shape[:2], dtype=np.float)
    for bool_map in bool_maps:
        attn_map += ndimage.binary_fill_holes(bool_map)
    attn_map /= N_THRESHOLDS

    # perform normalization
    l2_norm = np.sqrt((attn_map**2).sum())
    attn_map /= l2_norm
    attn_map /= attn_map.max()/255

    return attn_map.astype(np.uint8)

def main(args):
    """
        Entry point.
    """

    # load the image
    img = imread(args.input)
    if img.ndim == 2:
        img = gray2rgb(img)
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
