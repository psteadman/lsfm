#!/usr/bin/env python
# Josselyn-Frankland lab 2017
# author: pesteadman

# For input tif, add data to expand image in specified dimensions and directions

import skimage, scipy.ndimage, cv2, numpy
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i',dest='inputimage',
		help='Input image',default=None)
	parser.add_argument('-o',dest='outputimage',
		help='Default is to overwrite inputimage',default=None)
	parser.add_argument('-a', dest='dim0end', default=0, type=int)
	parser.add_argument('-b', dest='dim1end', default=0, type=int)
	parser.add_argument('-A', dest='dim0start', default=0, type=int)
	parser.add_argument('-B', dest='dim1start', default=0, type=int)
	parser.add_argument('--value',default=0,
		help='Value to pad image with, default 0')
	parser.add_argument('-v',dest='verbose',default=False,
		action='store_true', help='Verbose output')
	args = parser.parse_args()

	if args.inputimage == None:
		exit()

	padTup = ( (args.dim0start, args.dim0end), (args.dim1start, args.dim1end) )

	img_array = scipy.ndimage.imread(args.inputimage)
	img_padded = numpy.pad(img_array, padTup,'constant',constant_values=args.value)

	if args.outputimage != None:
		cv2.imwrite(args.outputimage, img_padded)
	else:
		cv2.imwrite(args.inputimage, img_padded)