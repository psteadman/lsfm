#!/usr/bin/env python

# code to stitch images and combined sheets
# given an input directory and imaging details

# Frankland lab 2017
# Contributors: Patrick Steadman

import argparse, os, glob, re
import numpy, json, cv2
import scipy.ndimage, skimage, skimage.exposure

def stitch_images(img1, img2, paramOverlap, paramArrangement, paramBlending):
	'''
	Stitches two images together
	Assumes first image then second image is order for stitching

	paramOverlap:
		Number of pixels for overlap
	paramArrangement:
		axis to blend in. 0 for y, 1 for x
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

	print("input shapes: ", img1.shape, img2.shape)
	if paramArrangement == 0: #y
		img1_ol 	= img1[int(img1.shape[paramArrangement] - paramOverlap):img1.shape[paramArrangement],
					 : ]
		img2_ol 	= img2[0:int(paramOverlap),
					 : ]
		img1_residual	= img1[0:int(img1.shape[paramArrangement] - paramOverlap),
					 : ]
		img2_residual = img2[int(paramOverlap):img2.shape[paramArrangement],
					 : ]
	if paramArrangement == 1: #x
		img1_ol 	= img1[: , 
				int(img1.shape[paramArrangement] - paramOverlap):img1.shape[paramArrangement] ]
		img2_ol 	= img2[ : , 
				0:int(paramOverlap) ]
		img1_residual	= img1[ : , 
				0:int(img1.shape[paramArrangement] - paramOverlap) ]
		img2_residual = img2[ : ,
				int(paramOverlap):img2.shape[paramArrangement] ]

	print("input ol shapes: ", img1_ol.shape, img2_ol.shape)
	print("input residual shapes: ", img1_residual.shape, img2_residual.shape)

	if paramBlending == 0: 
		img_ol = numpy.average(numpy.dstack((img1_ol,img2_ol)), axis=2, 
				weights=numpy.full(numpy.dstack((img1_ol,img2_ol)).shape, 1.5) ) # blending param of 1.5
	elif paramBlending == 1: 
		img_ol = numpy.mean(numpy.dstack((img1_ol,img2_ol)), 2)
	elif paramBlending == 2:
		img_ol = numpy.median(numpy.dstack((img1_ol,img2_ol)), 2)
	elif paramBlending == 3: 
		img_ol = numpy.amax(numpy.dstack((img1_ol,img2_ol)), 2)
	elif paramBlending == 4:
		img_ol = numpy.amin(numpy.dstack((img1_ol,img2_ol)), 2)
	else:
		print('incorrect blending options given, choose from: {}').format(listParamBlending)

	# Put the images together - this doesnt seem to be the best way, oddly?
	print("output shape: ", numpy.concatenate((img1_residual, img_ol, img2_residual), axis=paramArrangement).shape )
	return( numpy.concatenate((img1_residual, img_ol, img2_residual), axis=paramArrangement) )

def stitch_images_v2(img1, img2, paramOverlap, paramArrangement, paramBlending):
    if paramArrangement == 0: #y
        padTupA = ((0, int(img1.shape[paramArrangement] - paramOverlap)),(0,0))
        padTupB = ((int(img2.shape[paramArrangement] - paramOverlap),0),(0,0))
    if paramArrangement == 1: #x
        padTupA = ((0,0),(0, int(img1.shape[paramArrangement] - paramOverlap)))
        padTupB = ((0,0),(int(img2.shape[paramArrangement] - paramOverlap),0))
    print(padTupA)
    print(padTupB)
    a, b = (skimage.util.pad(img1, padTupA,'constant'), 
    skimage.util.pad(img2, padTupB,'constant'))
    c = numpy.amax(numpy.dstack((a,b)), axis=2)
    c = numpy.ma.average(numpy.dstack((a,b)), axis=2, 
                weights=numpy.dstack((a>0,b>0)).astype('float32')*1.5 )
    return(c)

def stitch_seq_image_list(imglist,paramOverlap,paramArrangement,paramBlending):
	# assume list is in order
	tmplist = imglist
	for x in range(len(tmplist)-1):
		tmplist[0] = stitch_images(tmplist[0],tmplist[x+1],paramOverlap,paramArrangement,paramBlending)

		# tmplist = [ stitch_images(tmplist[x],tmplist[x+1],paramOverlap,paramArrangement,paramBlending) for x in range(len(tmplist)) ]		
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
	parser.add_argument('-o','--output-directory',dest='outputdir',
		help='Directory where output directories of the z-stack \
		will be created for each channel')
	parser.add_argument('-j','--header-json',dest='imageheader',
		help='json file with image meta-data',default=None)
	args = parser.parse_args()

	if args.imageheader is not None:
		with open(args.imageheader,'r') as fp:
			imageHeader = json.load(fp)
			stepsX = imageHeader["stepsX"]
			stepsY = imageHeader["stepsY"]
			stepsZ = imageHeader["stepsZ"]
			nChannels = imageHeader["nChannels"]
			nSheets = imageHeader["nSheets"]
			overlap = imageHeader["overlap"]
			imageName = imageHeader["imageName"]
			paramBlending = imageHeader["paramBlending"]
	else:
		print("Missing header json file")

	# handle output directory create for each channel
	outputdirList = [0 for x in range(nChannels)]
	for i in range(nChannels):
		outputdirList[i] = args.outputdir+"/"+imageName+"_Channel"+str(i)+"/" 
		print(outputdirList[i])
		if not os.path.isdir(outputdirList[i]):
			os.mkdir(outputdirList[i])

	for r in range(stepsZ): 
		# fault in that r starts at 0 so stepsZ must be 1 more than last Z
		# find files in that step
		# assumes tif file and z is the only 4 digit number.
		filesZ = glob.glob(args.inputdir+"/*Z"+str(r).zfill(4)+"*.???")
		# print(stepsZ, r, filesZ)
		
		# separate by channel
		for channel in range(nChannels):
			if nChannels > 1:
				patternChannel = re.compile( "Filter"+str(channel).zfill(4) )
				filesZsingleChannel = [image for image in filesZ if patternChannel.search(image) != None]
			else:
				filesZsingleChannel = filesZ
			# if no files at z-step break this iteration
			if len(filesZsingleChannel) < 1:
				break
			
			# empty list for images to be put in
			imagesZsingleChannelX_stitchedY = [0 for x in range(stepsX)]
			
			# separate by tile
			for tileX in range(stepsX):
				print("running tileX: "+str(tileX))
				patternX = re.compile( "\["+str(tileX).zfill(2)+" x " )
				filesZsingleTileX = [image for image in filesZsingleChannel if patternX.search(image) != None]

				# empty list for images to be put in
				imagesZsingleChannelY = [0 for y in range(stepsY)]

				for tileY in range (stepsY):
					print("running tileY: "+str(tileY))
					patternY = re.compile( "\["+str(tileX).zfill(2)+" x "+str(tileY).zfill(2)+"\]" )
					filesZsingleTileXY = [image for image in filesZsingleTileX if patternY.search(image) != None]
					print(filesZsingleTileXY)

					if len(filesZsingleTileXY) == 2:
						# we have 2 sheets and we combine based on max
						#imagesZsingleChannelY[tileY] = skimage.exposure.rescale_intensity( 
						imagesZsingleChannelY[tileY] =	numpy.amax( numpy.dstack((
							scipy.ndimage.imread(filesZsingleTileXY[0], flatten=True),
							scipy.ndimage.imread(filesZsingleTileXY[1], flatten=True) )),
							2)
						#, out_range=(0, 1) )
						# Should I check these at 16 bit images when I read them in?
					elif len(filesZsingleTileXY) == 1:
						# imagesZsingleChannelY[tileY] = skimage.exposure.rescale_intensity(
						imagesZsingleChannelY[tileY] =	scipy.ndimage.imread(filesZsingleTileXY[0], flatten=True)
							#, out_range=(0, 1) )
					else:
						print("Something went wrong in combining sheets")

				# stitch the Ys together
				overlapY = numpy.around(overlap*imagesZsingleChannelY[0].shape[0])
				print("Overlap in Y: " + str(overlapY))
				imagesZsingleChannelX_stitchedY[tileX] = stitch_seq_image_list(imagesZsingleChannelY,overlapY,0,paramBlending)
				print(imagesZsingleChannelX_stitchedY[tileX].shape)
				print(imagesZsingleChannelX_stitchedY[tileX].dtype)

			# stitch the Xs together - generalize for any number of X positions
			overlapX = numpy.around(overlap*imagesZsingleChannelX_stitchedY[0].shape[1])
			print("Overlap in X: " + str(overlapX))
			imageZsingleChannel = stitch_seq_image_list(imagesZsingleChannelX_stitchedY,overlapX,1,paramBlending)
			print(imageZsingleChannel.min())
			print(imageZsingleChannel.max())
			print(imageZsingleChannel.dtype)
			imageZsingleChannel = skimage.exposure.rescale_intensity(imageZsingleChannel, out_range=(0, 1) )
			print(imageZsingleChannel.min())
			print(imageZsingleChannel.max())
			print(imageZsingleChannel.dtype)

			out = outputdirList[channel]+imageName+'_'+str(r).zfill(4)+'.tif' 
			print(out); cv2.imwrite(out,skimage.img_as_uint(imageZsingleChannel))
		
# image info patterns is [?? x ??] use this as its constant (as long as we have x and y devices used)
# stitch images together (and repeat for other sheet)
# write stitched and merged z-stack[r] image to channel directory
# save with cv2 so 16 bit