#!/usr/bin/env python

# code to stitch images and then combined sheets
# given an input directory and imaging details

# Frankland lab 2017
# Contributors: Patrick Steadman

import argparse, os, glob, re
import numpy, json

import skimage
import scipy.misc
import cv2

def stitch_images(img1, img2, paramOverlap, paramArrangement, paramBlending):
	'''
	Stitches two images together

	paramOverlap:
		percent of images that overlap
	paramArrangement:
		axis to blend in. 0 for x, 1 for y
	paramBlending:
	1 Linear blending: In the overlapping area the intensity 
		are smoothly adjusted between the two images.
		opencv cv2.AddWeighted() 
		see -> http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html
	2 Average: In the overlapping area the average intensity 
		between all images is computed (example source code).
	3 Median: In the overlapping area the median intensity of 
		all images is computed.
	4 Max. Intensity: In the overlapping area the maximum 
		intensity between all images is used int the output image.
	5 Min. Intensity: In the overlapping area the minimum 
		intensity between all images is used int the output image.
	'''

	# double check these tuples end up correct
	# we assume first image then second image is order for stitch
	img1_ol = ( img1.shape[paramArrangement] - img1.shape[paramArrangement]*paramOverlap, 
				img1.shape[paramArrangement] )
	img2_ol = ( 0, img2.shape[paramArrangement]*paramOverlap )

	img1_top    = ( 0, img1.shape[paramArrangement] - img1.shape[paramArrangement]*paramOverlap )
	img2_bottom = (img2.shape[paramArrangement]*paramOverlap, 
				   img2.shape[paramArrangement] )

	listParamBlending = ['blend','mean','median','max','min']
	if paramBlending == listParamBlending[0]:
		# blending param of 1.5 
		img_ol = numpy.average(numpy.dstack(img1_ol,img2_ol),axis=2, 
				weights=numpy.full(numpy.dstack((img1_ol,img2_ol)).shape, 1.5) )
	elif paramBlending == listParamBlending[1]:
		img_ol = numpy.mean(numpy.dstack((img1_ol,img2_ol)),2)
	elif paramBlending == listParamBlending[2]:
		img_ol = numpy.median(numpy.dstack((img1_ol,img2_ol)),2)
	elif paramBlending == listParamBlending[3]:
		img_ol = numpy.max(numpy.dstack((img1_ol,img2_ol)),2)
	elif paramBlending == listParamBlending[4]:
		img_ol = numpy.min(numpy.dstack((img1_ol,img2_ol)),2)
	else:
		print('incorrect blending options given, choose from: {}').format(listParamBlending)

	# Put the images together
	img_stitched = numpy.concatenate(img1_top, img_ol,, img2_bottom paramArrangement)


if __name__ == "__main__":
	description = """
	Input is directory containing images from LSFM
	Output is directories containing z-stack of stitched and combined images for each channel
	"""
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-i','--input-directory',dest='inputdir',
		help='LSFM raw stack directory')
	parser.add_argument('-o','--output-directory',dest='outputdir'
		help='Directory where output directories of the z-stack \
		will be created for each channel')
	parser.add_argument('-h','--header-json',dest='imageheader',
		help='json file with image meta-data',default=None)
	args = parser.parse_args()

	if args.imageheader is not None:
        with open(args.imageheader,'r') as fp:
            imageHeader = json.load(fp)
            stepsX = imageHeader["stepsX"]
            stepsY = imageHeader["stepsY"]
            stepsZ = imageheader["stepsZ"]
            nChannels = imageheader["nChannels"]
            nSheets = imageheader["nSheets"]
            overlap = imageHeader["overlap"]
            imageName = imageHeader["imageName"]
    else:
        print("Missing header json file")

    # handle output directory create for each channel
	for i in range(1,nChannels):
		outputdirList[i] = args.outputdir+"/"+imageName+"_channel"+str(i) 
		os.mkdir(outputdirList[i])

	for r in range(stepsZ):
		
		# find files in that step
		filesZ = glob.glob(args.inputdir+"/*/"+str(r).zfill(4)+"*.tif")
		
		# separate by channel
		for channel in nChannels:
			re.compile( "UltraFilter"+str(channel).zfill(4) )
			filesZsingleChannel = [image for image in filesZ if re.search(image) != None]
			
			# separate by light sheet
			for sheet in range(1):
				re.compile( "C"+str(sheet).zfill(2) )
				filesZsingleChannelsingleSheet = [image for image in filesZsingleChannel if re.search(image) != None]

				# read in images
				filename = os.path.basename(args.imgs[r],'.tif') #helpful?
				img = scipy.ndimage.imread(args.imgs[r], flatten=True) 
				# confirm 16 bit with dtype
		# image info patterns is [?? x ??] use this as its constant (as long as we have x and y devices used)
		
		# stitch images together (and repeat for other sheet)
		# for stepsX stitch
		for x in range(stepsX-1):
			# img1[x], img2[x+1]
			img_x = stitch_images(img1, img2, overlap, 0, 0)
		# for output and stepsY stitch

		# merge sheets based on max intensities

		# write stitched and merged z-stack[r] image to channel directory
		# save with cv2 so 16 bit
		out = args.outputdir+filename+'_'+str(r.zfill(4))+'.tif' 
		print(out); scipy.misc.imsave(out,img)

