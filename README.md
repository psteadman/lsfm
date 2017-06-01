#README

## STATUS - DOES NOT WORK PROPERLY. Details below. 

I should create a circle image and then cut it myself with known overlap this will create a true test set. 

I have a 512 x 512 image that I will split to make a test case. If I want the image overlap to be 20% what should be the dimensions of each tile for that image?
I did the split by 10%, so each image gets 10% extra of half so total overlap space should be 20%. Though the stitching only works properly if I use overlap of 18%. I cant figure out why.

Since I've played with a test set of 2x2 and 3x3 that works. This is a contrived set I created myself. For real data I have tried and had mixed results. To some extent test set 2 appears to work with overlap set at 0.22 instead of 0.2. I can not get test set 1 or 3 to work in a satisfactory way. There is something off about the math in doing the overlap and stitching which has yet to reveal its self to my eyes...