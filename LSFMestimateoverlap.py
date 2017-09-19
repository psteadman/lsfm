#!/usr/bin/env python
# Josselyn-Frankland lab 2017
# author: pesteadman

# assumes tiles/images are all the same size

# 2560 x 2160 - tile dims
# 4608 x 5616 - 20% ol stitched dims

import numpy
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# parser.add_argument('--intended',dest='intendedOLAxis', type=int,
	# 	help='Intended overlap in FIJI output of stitched image axis in pixels')
	parser.add_argument('--computed',dest='computedAxis', type=int, default=0,
		help='Estimate overlap in FIJI output of stitched image axis in pixels')
	parser.add_argument('--tile',dest='originalTileAxis', type=int,
		help='Raw tile image axis in pixels', default=2160)
	parser.add_argument('--ntiles',dest='numberOfTiles', type=int,
		help='Number of tiles along the axis given in --tile for the final stitched image', default=3)
	args = parser.parse_args()
		
	if args.computedAxis == 0:
		print("Need to give estimate overlap axis value"); exit()

	nOverlaps = 2*(args.numberOfTiles-1)
	est_ol = 2*(args.numberOfTiles*args.originalTileAxis - args.computedAxis)/(nOverlaps*args.originalTileAxis)
	print(numpy.round(est_ol, decimals=3))

