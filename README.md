#README

## STATUS - in development.

This is not operational at the moment

512 x 512 image split to make a test case.

![alt text](./testSet/circlesBrightDark.png?raw=true "Test image")

## Results as of 2017-09

Test set of 2x2 and 3x3 works with 0.18 overlap. This is the correct overlap for an output image of 512 x 512. 
``` sh
./LSFMestimateoverlap.py --computed 512 --tile 282 --ntiles 2
0.184
```

There is something off about the math in doing the overlap and stitching which has yet to reveal its self to my eyes...

For real data I have tried and had mixed results. To some extent test set 2 appears to work with overlap set at 0.22 instead of 0.2. I can not get test set 1 or 3 to work in a satisfactory way.

Further when tiles overlap there is an intensity difference that is noticeable. 