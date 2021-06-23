usage:

python converter.py
or
python /path/to/converter.py

changes from version 0.02

*fixed handling of regular expressions and spaces in filenames on merge tab
*add initial version of video conversion tab

This version should be functional and usable if you have required programs in command path

programs needed for full functionality:

pygtk
mplayer
mencoder
ffmpeg
lame
oggenc
mppenc
faac
flac

TODO:

add bitrate option in audio from video and audio to audio tabs
add copy option for audio and video codecs in video to video tab
support audio copy in video merge
support different containers in video merge if possible
support different containers in split tab if possible
provide better option/control over output file
