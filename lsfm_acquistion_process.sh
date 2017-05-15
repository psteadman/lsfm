#!/usr/bin/env bash

# code to stitch and combine L and R sheet from LSFM

# Frankland lab 2017
# Contributors: Patrick Steadman


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

for folder in 17f-17*; do 

echo "IMAGE" $folder; 
cd $folder;
echo "STARTING DIRECTORY" $PWD
rename "s/ //g" s0/*
rename "s/ //g" s1/*
if [[ -d s1 ]] ; then
echo s1 exists
for file in s1/*_????.tif; do 
dir=`dirname $file`; 
base=`basename $file .tif`; 
mv $file ${dir}/${base}_s1.tif
done
fi

if [[ -d s0 ]] ; then
echo s0 exists
for file in s0/*_????.tif; do 
dir=`dirname $file`; 
base=`basename $file .tif`; 
mv $file ${dir}/${base}_s0.tif
done
mkdir combined
fiji --headless -macro ~/Dropbox/mbp/bin/combineSheets.ijm /media/psteadman/lightsheetZF1/LSFM_Data/Atlas/stitched_data/${folder}/s0/:/media/psteadman/lightsheetZF1/LSFM_Data/Atlas/stitched_data/${folder}/s1/:/media/psteadman/lightsheetZF1/LSFM_Data/Atlas/stitched_data/${folder}/combined/;
fi

cd -
done