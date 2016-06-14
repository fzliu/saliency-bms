# saliency-bms

## Introduction

This is an implementation of the Boolean Map Saliency algorithm, by Jianming Zhang and Stan Sclaroff, with slight modifications. You can read the paper here: http://cs-people.bu.edu/jmzhang/BMS/BMS_iccv13_preprint.pdf.

## Requirements

 - Python >= 2.7
 - OpenCV >= 2.4 (with Python bindings)

## Usage

```
python saliency.py -i <image_path>
```

This will output a saliency image in the same directory as the input image.

## Sample

Upper two images are [apple](https://www.flickr.com/photos/torange-biz/14784889249) by Valdemar Fishmen and [Golden Gate Bridge with Reflections](https://www.flickr.com/photos/louisraphael/16170941243) by Louis Raphael. Originals are on the left, while full-resolution saliency results are on the right.

<p align="center">
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/apple.jpg" width="40%"/>
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/apple_saliency.jpg" width="40%"/>
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/golden_gate.jpg" width="40%"/>
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/golden_gate_saliency.jpg" width="40%"/>
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/frank.jpg" width="40%"/>
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/frank_saliency.jpg" width="40%"/>
</p>

The algorithm works for more than just natural images. Here's a saliency example on fan artwork from [/r/Overwatch](http://www.reddit.com/r/Overwatch) (credit goes to [GreenTaldarin](http://greentaldarin.deviantart.com)):

<p align="center">
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/reaper.jpg" width="40%"/>
<img src="https://raw.githubusercontent.com/fzliu/saliency-bms/master/images/reaper_saliency.jpg" width="40%"/>
</p>
