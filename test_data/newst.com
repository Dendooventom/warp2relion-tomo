# THIS IS A COMMAND FILE TO MAKE AN ALIGNED STACK FROM THE ORIGINAL STACK
#
####CreatedVersion####4.10.49
#
# It assumes that the views are in order in the image stack
#  
# The size argument should be ,, for the full area or specify the desired 
# size (e.g.: ,10)
#
# The offset argument should be 0,0 for no offset, 0,300 to take an area
# 300 pixels above the center, etc.
#
$setenv IMOD_OUTPUT_FORMAT MRC
$newstack -StandardInput
AntialiasFilter	-1
InputFile	TS_05.mrc.st
OutputFile	TS_05.mrc_ali.mrc
TransformFile	TS_05.mrc.xf
TaperAtFill	1,1
AdjustOrigin	
SizeToOutputInXandY	512,720
OffsetsInXandY	0.0,0.0
#DistortionField	.idf
ImagesAreBinned	1.0
BinByFactor	8
#GradientFile	TS_05.mrc.maggrad
$if (-e ./savework) ./savework
