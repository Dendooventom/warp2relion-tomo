# Command file to run Tilt
#
####CreatedVersion####4.10.49
# 
# RADIAL specifies the frequency at which the Gaussian low pass filter begins
#   followed by the standard deviation of the Gaussian roll-off
#
# LOG takes the logarithm of tilt data after adding the given value
#
$setenv IMOD_OUTPUT_FORMAT MRC
$tilt -StandardInput
InputProjections TS_05.mrc_ali.mrc
OutputFile TS_05.mrc_full_rec.mrc
IMAGEBINNED 8
TILTFILE TS_05.mrc.tlt
THICKNESS 2700
RADIAL 0.35 0.035
FalloffIsTrueSigma 1
XAXISTILT 0.0
SCALE 0.0 0.05
PERPENDICULAR 
MODE 2
FULLIMAGE 4092 5760
SUBSETSTART -2 0
AdjustOrigin 
ActionIfGPUFails 1,2
XTILTFILE TS_05.mrc.xtilt
LOCALFILE TS_05.mrclocal.xf
OFFSET 0.0
SHIFT 0.0 0.0
FakeSIRTiterations 10
$if (-e ./savework) ./savework
