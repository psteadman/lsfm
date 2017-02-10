#!/usr/bin/env bash

# code to stitch and combine L and R sheet from LSFM

# Patrick Steadman 2016


outputdir=$2

mkdir $outputdir
cd $outputdir
mkdir s0; mkdir s1; mkdir combined

# call stitching script for each sheet



# rename files for L+R combining
cd $outputdir
rename "s/ //g" s0/*
rename "s/ //g" s1/*
for file in s0/*; do dir=`dirname $file`; base=`basename $file .tif`; mv $file ${dir}/${base}_s0.tif; done
for file in s1/*; do dir=`dirname $file`; base=`basename $file .tif`; mv $file ${dir}/${base}_s1.tif; done

# combine L and R sheets
echo fiji --headless -macro ~/Dropbox/mbp/bin/combineSheets.ijm \
'${outputdir}/s0/:${outputdir}/s1/:${outputdir}/combined/'

# if combining is successful remove s0 and s1 stacks - maybe dont do this

# is there a way to combine tif stack to hdf5 file format