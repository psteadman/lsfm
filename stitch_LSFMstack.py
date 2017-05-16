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
	0 Linear blending: In the overlapping area the intensity 
		are smoothly adjusted between the two images.
		opencv cv2.AddWeighted() 
		see -> http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html
	1 Average: In the overlapping area the average intensity 
		between all images is computed (example source code).
	2 Median: In the overlapping area the median intensity of 
		all images is computed.
	3 Max. Intensity: In the overlapping area the maximum 
		intensity between all images is used int the output image.
	4 Min. Intensity: In the overlapping area the minimum 
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
	if paramBlending == 0: #listParamBlending[0]:
		# blending param of 1.5 
		img_ol = numpy.average(numpy.dstack(img1_ol,img2_ol),axis=2, 
				weights=numpy.full(numpy.dstack((img1_ol,img2_ol)).shape, 1.5) )
	elif paramBlending == 1: #listParamBlending[1]:
		img_ol = numpy.mean(numpy.dstack((img1_ol,img2_ol)),2)
	elif paramBlending == 2: #listParamBlending[2]:
		img_ol = numpy.median(numpy.dstack((img1_ol,img2_ol)),2)
	elif paramBlending == 3: #listParamBlending[3]:
		img_ol = numpy.max(numpy.dstack((img1_ol,img2_ol)),2)
	elif paramBlending == 4: #listParamBlending[4]:
		img_ol = numpy.min(numpy.dstack((img1_ol,img2_ol)),2)
	else:
		print('incorrect blending options given, choose from: {}').format(listParamBlending)

	# Put the images together
	return( numpy.concatenate(img1_top, img_ol, img2_bottom, paramArrangement) )

def stitch_seq_image_list(imglist,paramOverlap,paramArrangement,paramBlending):
	# assume list is in order
	tmplist = imglist
	# if only 1 step thus 1 image should skip while loop?
	while len(tmplist > 1):
		tmplist = [stitch_images(tmplist[x],tmplist[x+1],paramOverlap,paramArrangement,paramBlending) for x in range(len(tmplist-1))]		
	# return the final image
	return(tmplist[0])

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
            paramBlending = imageHeader["paramBlending"]
    else:
        print("Missing header json file")

    # handle output directory create for each channel
	for i in range(1,nChannels):
		outputdirList[i] = args.outputdir+"/"+imageName+"_channel"+str(i)+"/" 
		os.mkdir(outputdirList[i])

	for r in range(stepsZ): 
		# find files in that step
		filesZ = glob.glob(args.inputdir+"/*/"+str(r).zfill(4)+"*.tif")
		
		# separate by channel
		for channel in nChannels:
			re.compile( "UltraFilter"+str(channel).zfill(4) )
			filesZsingleChannel = [image for image in filesZ if re.search(image) != None]
			
			# empty list for images to be put in
			imagesZsingleChannelX_stitchedY = [0 for x in range(stepsX-1)]
			
			# separate by tile
			for tileX in range(stepsX-1):
				re.compile( "["+str(tileX).zfill(2)+" x " )
				filesZsingleTileX = [image for image in filesZsingleChannel if re.search(image) != None]
				
				# empty list for images to be put in
				imagesZsingleChannelY = [0 for y in range(stepsY-1)]

				for tileY in range (stepsY-1):
					re.compile( "["+str(tileX).zfill(2)+" x "+str(tileY).zfill(2)+"]" )
					filesZsingleTileXY = [image for image in filesZsingleTileX if re.search(image) != None]
					
					if len(filesZsingleTileXY == 2):
						# we have 2 sheets and we combine based on max
						imagesZsingleChannelY[tileY] = numpy.max( numpy.dstack(
							scipy.ndimage.imread(filesZsingleTileXY[0], flatten=True),
							scipy.ndimage.imread(filesZsingleTileXY[1], flatten=True) ),
							2)
						# Should I check these at 16 bit images when I read them in?
					elif len(filesZsingleTileXY == 1):
						imagesZsingleChannelY[tileY] = scipy.ndimage.imread(filesZsingleTileXY[0], flatten=True)
					else:
						print("Something went wrong in combining sheets")


				# stitch the Ys together
				imagesZsingleChannelX_stitchedY[tileX] = stitch_seq_image_list(imagesZsingleChannelY,overlap,1,paramBlending)

			# stitch the Xs together - generalize for any number of X positions
			imageZsingleChannel = stitch_seq_image_list(imagesZsingleChannelX_stitchedY,overlap,0,paramBlending)
			out = outputdirList[channel]+filename+'_'+str(r.zfill(4))+'.tif' 
			print(out); cv2.imwrite(out,imageZsingleChannel)
		
# image info patterns is [?? x ??] use this as its constant (as long as we have x and y devices used)
# stitch images together (and repeat for other sheet)
# write stitched and merged z-stack[r] image to channel directory
# save with cv2 so 16 bit