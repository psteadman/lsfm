#!/usr/bin/env python

# code to stitch images and then combined sheets
# given an input directory and imaging details

# Patrick Steadman 2016
import argparse
import skimage
import scipy.misc
import os, sys
import numpy
import cv2

def stitch_images(paramOverlap, paramArrangement, paramBlending, imgList):
	'''
	This function input list of images on a single x-y plane of a z-stack
	and stitch them according to a defined overlap and arrangement parameter

	Blending of overlap region algorithm
	- Linear blending: In the overlapping area the intensity 
		are smoothly adjusted between the two images.
		opencv cv2.AddWeighted() does this
	- Average: In the overlapping area the average intensity 
		between all images is computed (example source code).
	- Median: In the overlapping area the median intensity of 
		all images is computed.
	- Max. Intensity: In the overlapping area the maximum 
		intensity between all images is used int the output image.
	- Min. Intensity: In the overlapping area the minimum 
		intensity between all images is used int the output image.
	'''

	numpy.concatenate(img1,img2,0) # for x
	numpy.concatenate(img1,img2,1) # for y
	


if __name__ == "__main__":
	description = """
	Program to take light-sheet microscope z-stack and print image information
	"""
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-i','--input-directory',
		help='LSFM raw stack directory')
	parser.add_argument('imgs',nargs='+')
	parser.add_argument('-o','--output-directory',help='output csv file')
	args = parser.parse_args()

	# such a simple script
	filename = os.path.basename(args[0])
	img = scipy.ndimage.imread(args[0], flatten=True)  
	scipy.misc.imsave(args[1],img)

