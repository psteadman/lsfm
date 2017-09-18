#!/usr/bin/env python
# Josselyn-Frankland lab 2017
# author: pesteadman

# input is folder with stack of tifs from FIJI where compute overlap option was used
# Finds largest of each dimension and zero pads all others to the same dimensions
# Zero pads an equal amount in both directions

import skimage, scipy.ndimage, cv2, numpy
import argparse, glob, os 

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input-directory',dest='inputdir',
		help='Stitched image stack directory',default=None)
	parser.add_argument('-o','--output-directory',dest='outputdir',
		help='Output directory',default=None)
	parser.add_argument('-v',dest='verbose',default=False,
		action='store_true')
	args = parser.parse_args()

	if args.inputdir == None:
		exit()
	if args.outputdir != None and not os.path.isdir(args.outputdir):
		os.mkdir(args.outputdir)

	imgList = glob.glob(args.inputdir+"/*.tif")
	imgLargestDim = [0, 0]
	print("Reading {} images to find the largest slice...".format(len(imgList)))

	for img in imgList:
		img_array = scipy.ndimage.imread(img)
		if (imgLargestDim[0] < img_array.shape[0]):
			imgLargestDim[0] = img_array.shape[0]
		if (imgLargestDim[1] < img_array.shape[1]):
			imgLargestDim[1] = img_array.shape[1]

	print("Largest slice dimensions: {} {}".format(imgLargestDim[0], imgLargestDim[1]) )

	for img in imgList:
		img_array = scipy.ndimage.imread(img)
		# determine pad size, little issue in divide by 2 and round can cause new dims to be off by 1
		# hack solution is to solve by adding 1 to the end within the while loop until they match...
		extraDim0 = -1; extraDim1 = -1
		padDim0 = int(numpy.round((imgLargestDim[0] - img_array.shape[0])/2))
		padDim1 = int(numpy.round((imgLargestDim[1] - img_array.shape[1])/2))
		while (padDim0 + padDim0 + img_array.shape[0]) + extraDim0 < imgLargestDim[0]:
			extraDim0 += 1
		while (padDim1 + padDim1 + img_array.shape[1]) + extraDim1 < imgLargestDim[1]:
			extraDim1 += 1
		padTup = ( (padDim0, padDim0 + extraDim0), (padDim1, padDim1 + extraDim1) )
		# send out some details to the user 
		if args.verbose == True:
			print("Original size {}".format(img_array.shape), end=' ')
			print("Padded tuple {}".format(padTup), end=' ')
			print("Final dim {} {}".format((padDim0 + padDim0 + img_array.shape[0] + extraDim0), 
							(padDim1 + padDim1 + img_array.shape[1] + extraDim1)), end=' ')
			print("Writing padded image {}".format(img[-8:-4]), end='\n', flush=True);
		img_padded = numpy.pad(img_array,padTup,'constant',constant_values=100)
		if args.outputdir != None:
			cv2.imwrite(args.outputdir+"/"+os.path.basename(img), img_padded)
		else:
			cv2.imwrite(img, img_padded)
	print("Last image's final dimensions as a check: {}".format(img_padded.shape) )

