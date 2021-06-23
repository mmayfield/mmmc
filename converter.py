#!/usr/bin/env python

#    Written by Mark Mayfield. MMMC uses support programs to perform a 
#    variety of multimedia conversions.
#    Copyright (C) 2012  Mark Mayfield
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk, gobject, re, os, pwd, sys, subprocess, math, time, random

file_name = sys.path[0] + "/Multimedia.png"
home = pwd.getpwuid(os.getuid()).pw_dir

class MMMC:

    def filechoose(self, widget):
	chooser = gtk.FileChooserDialog(title="Output Filename - Only .avi extension!",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK))
	chooser.set_icon_from_file(file_name)
	response = chooser.run()
	if response == gtk.RESPONSE_OK:
		filename = chooser.get_filename()
		chooser.destroy()
		self.merge(filename)
	elif response == gtk.RESPONSE_CANCEL:
		chooser.destroy()

    def vidconvert(self, widget):
	vfile = re.escape(self.vidfile.get_text())
	container = str(self.container.get_active_text())
	outfile = os.path.splitext(vfile)[0] + '_converted.' + container
	aformat = str(self.aformat.get_active_text())
	vformat = str(self.vformat.get_active_text())
	abr = str(self.abr.get_active_text())
	vbr = str(self.vbr.get_active_text())
	scale = str(self.scale.get_active_text())
	index = scale.find('/')
	scale = scale[index+1:len(scale)]
	scale = scale.replace('x',':')
	if 'h264' in vformat:
		menvcopts = '-ovc x264 -x264encopts bitrate=' + vbr
		ffvopts = ' -vcodec libx264 -b ' + vbr + 'k -y '
	elif 'xvid' in vformat:
		menvcopts = '-ovc xvid -xvidencopts bitrate=' + vbr
		ffvopts = ' -vcodec libxvid -b ' + vbr + 'k -y '
	elif 'mpeg4' in vformat:
		menvcopts = '-ovc lavc -lavcopts vcodec=mpeg4:vbitrate=' + vbr
		ffvopts = ' -vcodec mpeg4 -b ' + vbr + 'k -y '
	elif 'wmv' in vformat:
		menvcopts = '-ovc lavc -lavcopts vcodec=wmv1:vbitrate=' + vbr
		ffvopts = ' -vcodec wmv1 -b ' + vbr + 'k -y '
	elif 'h263' in vformat:
		ffvopts = ' -vcodec h263 -b ' + vbr + 'k -y '
	elif 'flv' in vformat:
		ffvopts = ' -vcodec flv -b ' + vbr + 'k -y '
	elif 'theora' in vformat:
		ffvopts = ' -vcodec libtheora -b ' + vbr + 'k -y '
	elif 'rv20' in vformat:
		ffvopts = ' -vcodec rv20 -b ' + vbr + 'k -y '
	if 'ac3' in aformat:
		menacopts = '-oac lavc -lavcopts acodec=ac3:abitrate=' + abr
		ffaopts = '-acodec ac3 -ab ' + abr + 'k ' 
	elif 'aac' in aformat:
		menacopts = '-oac faac -faacopts br=' + abr
		ffaopts = '-acodec libfaac -ab ' + abr + 'k '
	elif 'mp3' in aformat:
		menacopts = '-oac mp3lame -lameopts vbr=3:br=' + abr
		ffaopts = '-acodec libmp3lame -ab ' + abr + 'k '
	elif 'wma' in aformat:
		menacopts = '-oac lavc -lavcopts acodec=wmav1:abitrate=' + abr
		ffaopts = '-acodec wmav1 -ab ' + abr + 'k '
	elif 'amr' in aformat:
		ffaopts = '-acodec libopencore_amrnb -ac 1 -ar 8000 -ab ' + abr + 'k '
	elif 'vorbis' in aformat:
		menacopts = '-oac lavc -lavcopts libvorbis -ab ' + abr + 'k -y '
		ffaopts = '-acodec libvorbis -ab ' + abr + 'k -y '
	elif 'RealAudio' in aformat:
		menacopts = '-oac lavc -lavcopts acodec=real_144 '
		ffaopts = '-acodec real_144 -ac 1 -ar 8000 -y '
	elif 'flac' in aformat:
		menacopts = '-oac lavc -lavcopts acodec=flac'
		ffaopts = '-acodec flac -y '
	part1 = 'ffmpeg -i ' + vfile + ' -s ' + scale
	if not 'None' in container and not 'None' in aformat and not 'None' in vformat and not 'None' in abr and not 'None' in vbr and not 'None' in scale:
		if '3gp' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
		elif 'avi' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' ' + menvcopts + ' ' + menacopts + ' -vf scale=' + scale + ' -o ' + outfile
		elif 'asf' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' ' + menvcopts + ' ' + menacopts + ' -of lavf -lavfopts format=asf -vf scale=' + scale + ' -o ' + outfile
		elif 'flv' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' -ovc lavc -lavcopts vcodec=flv:vbitrate=' + vbr + ' ' + menacopts + ' -of lavf -lavfopts format=flv -vf scale=' + scale + ' -o ' + outfile
		elif 'm4v' in container:
			if 'h264' in vformat:
				menvcopts += ':nocabac:global_header:frameref=3:threads=auto:bframes=0:subq=6:mixed-refs=0:weightb=0:8x8dct=1:me=umh:partitions=all:qp_step=4'
			cmd = part1 + ' -f ipod ' + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' -of lavf -lavfopts format=ipod ' + menvcopts + ' ' + menacopts + ' -vf scale=' + scale + ' -o ' + outfile
		elif 'mov' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' ' + menvcopts + ':keyint=200 ' + menacopts + ' -of lavf -lavfopts format=mov -vf scale=' + scale + ' -o ' + outfile
		elif 'mp4' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' -of lavf -lavfopts format=mp4 ' + menvcopts + ' ' + menacopts + ' -vf scale=' + scale + ' -o ' + outfile
		elif 'mkv' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' -of lavf -lavfopts format=matroska ' + menvcopts + ' ' + menacopts + ' -vf scale=' + scale + ' -o ' + outfile
		elif 'ogv' in container:
			cmd = part1 + ' -f ogg' + ffvopts + ffaopts + outfile
			cmd1 = 'ffmpeg -i ' + vfile + ' -y -f ogg -vcodec libtheora -b ' + vbr + 'k -acodec libvorbis -ab ' + abr + 'k -s ' + scale + ' ' + outfile
		elif 'rmv' in container:
			cmd = part1 + ' -f rm ' + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' -ovc lavc -lavcopts vcodec=rv10:vbitrate=' + vbr + ' ' + menacopts + ' -of lavf -lavfopts format=rm -vf scale=' + scale + ' -o ' + outfile
		elif 'swf' in container:
			cmd = part1 + ffvopts + ffaopts + outfile
			cmd1 = 'mencoder ' + vfile + ' -ovc lavc -lavcopts vcodec=flv:vbitrate=' + vbr + ' ' + menacopts + ' -of lavf -lavfopts format=swf -o ' + outfile
		elif 'psp' in container:
			cmd = part1 + ffvopts + ' -ar 24000 -f psp ' + ffaopts + re.sub('.psp','.mp4',outfile) + ' && ffmpeg -itsoffset -20 -i ' + vfile + ' -vcodec mjpeg -vframes 1 -an -f rawvideo -s 160:120 ' + re.sub('.psp','.THM',outfile)
		print cmd
		self.progress(cmd)

    def aset(self, widget):
	aformat = str(self.aformat.get_active_text())		
	abrstore = self.abr.get_model()
	abrstore.clear()
	if 'amr' in aformat:
		abrstore.append(["4.75"])
		abrstore.append(["5.15"])
		abrstore.append(["5.90"])
		abrstore.append(["6.70"])
		abrstore.append(["7.40"])
		abrstore.append(["7.95"])
		abrstore.append(["10.20"])
		abrstore.append(["12.20"])
	elif 'RealAudio' in aformat or 'flac' in aformat:
		abrstore.append(["N/A"])
	else:
		abrstore.append(["64"])
		abrstore.append(["96"])
		abrstore.append(["128"])
		abrstore.append(["196"])
		abrstore.append(["224"])
		abrstore.append(["320"])
	self.abr.set_model(abrstore)
	self.abr.set_active(0)

    def container_update(self, widget):
	scale = self.scale.get_active_text()
	fcontainer = str(self.container.get_active_text())
	aformat = str(self.aformat.get_active_text())
	liststore = self.vformat.get_model()
	liststore.clear()
	if 'flv' in fcontainer or 'swf' in fcontainer: 
		liststore.append(["flv"])
	if '3gp' in fcontainer:
		liststore.append(["h263"])
	if 'avi' in fcontainer or 'mp4' in fcontainer or 'mkv' in fcontainer or 'm4v' in fcontainer:
		liststore.append(["h264"])
	if 'ogv' in fcontainer or 'mkv' in fcontainer:
		liststore.append(["theora"])
	if 'asf' in fcontainer or 'mkv' in fcontainer:
		liststore.append(["wmv"])
	if 'avi' in fcontainer or 'mkv' in fcontainer or 'mp4' in fcontainer or 'm4v' in fcontainer:
		liststore.append(["xvid"])
	if 'mov' in fcontainer or 'avi' in fcontainer or 'mp4' in fcontainer or 'm4v' in fcontainer or 'psp' in fcontainer:
		liststore.append(["mpeg4"])
	if 'rmv' in fcontainer:
		liststore.append(["rv20"])
	self.vformat.set_model(liststore)
	self.vformat.set_active(0)
	audstore = self.aformat.get_model()
	audstore.clear()
	if '3gp' in fcontainer or 'avi' in fcontainer or 'mp4' in fcontainer or 'mkv' in fcontainer or 'flv' in fcontainer or 'm4v' in fcontainer or 'psp' in fcontainer:
		audstore.append(["aac"])
	if 'mov' in fcontainer or 'avi' in fcontainer or 'mkv' in fcontainer or 'rmv' in fcontainer:
		audstore.append(["ac3"])
	if 'avi' in fcontainer or 'flv' in fcontainer or 'swf' in fcontainer or 'mp4' in fcontainer or 'mkv' in fcontainer:
		audstore.append(["mp3"])
	if 'ogv' in fcontainer or 'mkv' in fcontainer:
		audstore.append(["vorbis"])
	if 'asf' in fcontainer or 'mkv' in fcontainer:
		audstore.append(["wma"])
	if '3gp' in fcontainer:
		audstore.append(["amr"])
	if 'rmv' in fcontainer:
		audstore.append(["RealAudio"])
	if 'mkv' in fcontainer:
		audstore.append(["flac"])
	self.aformat.set_model(audstore)
	self.aformat.set_active(0)
	vbrstore = self.vbr.get_model()
	vbrstore.clear()
	vbrstore.append(["512"])
	vbrstore.append(["756"])
	vbrstore.append(["1024"])
	vbrstore.append(["1250"])
	vbrstore.append(["1576"])
	self.vbr.set_model(vbrstore)
	self.vbr.set_active(0)
	self.aset("changed")
	vfile = str(self.vidfile.get_text())
	if os.path.exists(vfile):	
		cmd = "mplayer -noconfig all -cache-min 0 -vo null -ao null -frames 0 -identify " + re.escape(vfile) + " 2>/dev/null | grep VIDEO: | tr -s ' ' | cut -f 3 -d ' '"
		original = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(out, err) = original.communicate()
		original = str.strip('original/' + out)
		scalestore = self.scale.get_model()
		scalestore.clear()
		if not 'psp' in fcontainer and not '3gp' in fcontainer:
			scalestore.append([original])
		if not 'psp' in fcontainer:
			scalestore.append(["sqcif/128x96"])
			scalestore.append(["qcif/176x144"])
			scalestore.append(["cif/352x288"])
			scalestore.append(["4cif/704x576"])
			scalestore.append(["16cif/1408x1152"])
		if not '3gp' in fcontainer and not 'psp' in fcontainer:
			scalestore.append(["qqvga/160x120"])
		if not '3gp' in fcontainer:
			scalestore.append(["qvga/320x240"])
		if not '3gp' in fcontainer and not 'psp' in fcontainer:
			scalestore.append(["vga/640x480"])
			scalestore.append(["svga/800x600"])
			scalestore.append(["xga/1024x768"])
			scalestore.append(["uxga/1600x1200"])
			scalestore.append(["qxga/2048x1536"])
			scalestore.append(["sxga/1280x1024"])
			scalestore.append(["qsxga/2560x2048"])
			scalestore.append(["hsxga/5120x4096"])
			scalestore.append(["qvga/852x480"])
			scalestore.append(["wxga/1366x768"])
			scalestore.append(["wsxga/1600x1024"])
			scalestore.append(["wuxga/1920x1200"])
			scalestore.append(["woxga/2560x1600"])
			scalestore.append(["wqsxga/3200x2048"])
			scalestore.append(["wquxga/3840x2400"])
			scalestore.append(["whsxga/6400x4096"])
			scalestore.append(["whuxga/7680x4800"])
			scalestore.append(["cga/320x200"])
			scalestore.append(["ega/640x350"])
			scalestore.append(["hd480/852x480"])
			scalestore.append(["hd720/1280x720"])
			scalestore.append(["hd1080/1920x1080"])
		self.scale.set_model(scalestore)
		self.scale.set_active(0)
		for i, k in enumerate(scalestore):
			iter = scalestore.get_iter(i)
			if not 'None' in str(scale):
				if scalestore.get_value(iter,0) in scale:
					self.scale.set_active_iter(iter)

    def progress(self, cmd):
	self.window.hide()
	win = gtk.Window(gtk.WINDOW_TOPLEVEL)
	win.set_title('MMMC')
	win.set_deletable(0)
	win.set_icon_from_file(file_name)
	self.win = win
	waitframe = gtk.Frame()
	waitframe.set_border_width(25)
	waitframe.set_size_request(450, 200)
	waitlabel = gtk.Label("Job in Progress... Please Wait")
	pb = gtk.ProgressBar()
        self.pb = pb
        box = gtk.VBox()
	pbbox = gtk.HBox()
        self.win.show_all()
        self.keep_pulsing = False
        self.keep_pulsing = True
    	def do_pulse(*args):
        	if self.keep_pulsing:
        		self.pb.pulse()
           		return True
       		return False
	box.pack_start(waitlabel, padding=25)
	pbbox.pack_start(self.pb, padding=40)
        box.pack_start(pbbox, padding=25)
	waitframe.add(box)
	self.win.add(waitframe)
	self.win.show_all()
	gtk.gdk.flush()
	def tester():
		if p.poll() is None:
			return True
		else:
			self.win.destroy()
			self.window.show()
	gobject.idle_add(tester)
	p = subprocess.Popen(cmd, shell=True)
        gobject.timeout_add(200, do_pulse)

    def merge(self, filename):
	mergefiles = ''
	mergefiles = self.textbuffer.get_text(*self.textbuffer.get_bounds())
	files = ''
	for item in mergefiles.splitlines():
	        tmp = item.strip().lstrip()
        	files += re.escape(tmp) + ' '
	cmd = 'mencoder ' + files + ' -ovc copy -oac mp3lame -lameopts fast:preset=standard -o ' + re.escape(filename) + ' 2>' + home + '/errors.txt'
	self.progress(cmd)

    def	file_select(self, widget, contype):
	dialog = gtk.FileChooserDialog("Select File...",None,gtk.FILE_CHOOSER_ACTION_OPEN,
		(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	dialog.set_icon_from_file(file_name)
	dialog.set_default_response(gtk.RESPONSE_OK)
	filter = gtk.FileFilter()
	filter.set_name("All files")
	filter.add_pattern("*")
	dialog.add_filter(filter)
	vidfilter = gtk.FileFilter()
	imagefilter = gtk.FileFilter()
	vidfilter.set_name("Video Files")
	imagefilter.add_mime_type("image/png")
	imagefilter.add_mime_type("image/jpeg")
	imagefilter.add_mime_type("image/gif")
	vidfilter.add_pattern("*.flv")
	vidfilter.add_pattern("*.avi")
	vidfilter.add_pattern("*.mkv")
	vidfilter.add_pattern("*.ogv")
	vidfilter.add_pattern("*.mp4")
	vidfilter.add_pattern("*.mpeg")
	vidfilter.add_pattern("*.rmvb")
	vidfilter.add_pattern("*.rm")
	vidfilter.add_pattern("*.rmv")
	vidfilter.add_pattern("*.mov")
	vidfilter.add_pattern("*.3gp")
	vidfilter.add_pattern("*.asf")
	vidfilter.add_pattern("*.wmv")
	vidfilter.add_pattern("*.ogg")
	vidfilter.add_pattern("*.ogm")
	vidfilter.add_pattern("*.mpg")
	audfilter = gtk.FileFilter()
	audfilter.set_name("Audio Files")
	audfilter.add_pattern("*.mp3")
	audfilter.add_pattern("*.m4a")
	audfilter.add_pattern("*.aac")
	audfilter.add_pattern("*.ogg")
	audfilter.add_pattern("*.mpc")
	audfilter.add_pattern("*.wav")
	audfilter.add_pattern("*.flac")
	vidfilter.add_pattern("*.wma")
	dialog.add_filter(audfilter)
	dialog.add_filter(vidfilter)
	if 'audaud' in contype:
		dialog.set_filter(audfilter)
	elif 'merge' in contype or 'split' in contype or 'audvid' in contype or 'vidvid' in contype:
		dialog.set_filter(vidfilter)

	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		value = dialog.get_filename()
		if 'merge' in contype:
			(iter_first, iter_last) = self.textbuffer.get_bounds()
			if (re.escape(self.textbuffer.get_text(iter_first, iter_last)) == ''):
				value2 = value
			else:
				value2 = self.textbuffer.get_text(iter_first, iter_last) + ' \n' + value
			self.textbuffer.set_text(value2)
		elif 'split' in contype:
			self.splitentry.set_text(value)
		elif 'audvid' in contype:
			self.audvidentry.set_text(value)
		elif 'audaud' in contype:
			self.audaudentry.set_text(value)
		elif 'vidvid' in contype:
			self.vidfile.set_text(value)	
			aitem = self.aformat.get_active()
			abr = self.abr.get_active()
			vitem = self.vformat.get_active()
			vbr = self.vbr.get_active()
			self.container_update("changed")
			self.aformat.set_active(aitem)
			self.vformat.set_active(vitem)
			self.abr.set_active(abr)
			self.vbr.set_active(vbr)
	dialog.destroy()

    def split(self, widget):
	hours = int(self.entry2.get_text())
	minutes = int(self.entry3.get_text())
	total = (hours*60)+minutes
	cmd="mplayer -vo null -ao null -frames 0 -identify " + re.escape(self.splitentry.get_text()) + " | grep ID_LENGTH | cut -f 2 -d ="
	run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	length=0
	for line in run.stdout.readlines():
		if line != "":
			length = re.sub("\n", '', line)
	length = int(math.ceil(float(length)/60))
	if total > 0:
		base, ext = os.path.split(re.escape(self.splitentry.get_text()))
		newname2 = re.sub('[^.]+$', '',ext)
		newname3 = re.sub('\.', '',newname2)
		hourp = 00
		minp = 00
		count = 0
		part = 1
		cmd=''
		while ( count < length ):
			cmd += 'mencoder ' + re.escape(self.splitentry.get_text()) + ' -oac mp3lame -ovc copy -ss ' + str(hourp) + ':' + str(minp) + ':00 -endpos ' + str(hours) + ':' + str(minutes) + ':00 -o ' + home + '/Desktop/' + newname3 + '_part_' + str(part) + '.avi 2>' + home + '/errors.txt && '	
			count += total
			part += 1
			minp += total
			hourp = hourp + minp/60
			minp = minp%60
		cmd = cmd[:-3]
	self.progress(cmd)

    def clear(self, widget):
	self.textbuffer.set_text('')

    def bradio(self, contype):	

	box0 = gtk.VBox()
        box1 = gtk.VBox(False, 0)
        box0.pack_start(box1)
        box1.show()

        box2 = gtk.HBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()

        button = gtk.RadioButton(None, "mp3")
        button.connect("toggled", self.callback, contype, "mp3")
        box2.pack_start(button, True, True, 0)
        button.show()

        button = gtk.RadioButton(button, "aac")
        button.connect("toggled", self.callback, contype, "aac")
        box2.pack_start(button, True, True, 0)
        button.show()

        button = gtk.RadioButton(button, "ogg")
        button.connect("toggled", self.callback, contype, "ogg")
        box2.pack_start(button, True, True, 0)
        button.show()

        button = gtk.RadioButton(button, "mpc")
        button.connect("toggled", self.callback, contype, "mpc")
        box2.pack_start(button, True, True, 0)
        button.show()

        button = gtk.RadioButton(button, "flac")
        button.connect("toggled", self.callback, contype, "flac")
        box2.pack_start(button, True, True, 0)
        button.show()

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(25)
        box1.pack_start(box2, False, True, 0)
        box2.show()

        button.set_flags(gtk.CAN_DEFAULT)
        button.show()
	self.box0 = box0
        self.box0.show()

    def convert(self, widget, contype):
	cmd=''
	filename = ""	
	if 'audvid' in contype:
		filename = re.escape(self.audvidentry.get_text())
		base, ext = os.path.split(filename)
		name = re.sub('[^.]+$', '',ext) + 'wav'
		cmd = 'mplayer -nocorrect-pts -vc null -vo null -ao pcm:fast:file=' + home + '/Desktop/' + name + ' ' + filename + ' 2>' + home + '/errors.txt && '
		format = self.avformat.get_text()
	elif 'audaud' in contype:
		filename = re.escape(self.audaudentry.get_text())
		format = self.aaformat.get_text()	
	base, ext = os.path.split(filename)
	oldext = ext.split('.')[-1]
	name2 = re.sub('[^.]+$', '',ext)
	name3 = name2
	name2 += 'wav'
	if 'audvid' in contype:
		if 'mp3' in format:
			name3 += 'mp3'
			cmd += 'lame -b 192 ' + home + '/Desktop/' + name2 + ' ' + home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
		elif 'aac' in format:
			name3 += 'm4a'
			cmd += 'faac -w -s -b 192 -o ' + home + '/Desktop/' + name3 + ' ' + home + '/Desktop/' + name2 + ' 2>>' + home + '/errors.txt'
		elif 'ogg' in format:
			name3 += 'ogg'
			cmd += 'oggenc -q 5 ' + home + '/Desktop/' + name2 + ' -o '+ home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
		elif 'mpc' in format:
			name3 += 'mpc'
			cmd += 'mppenc --overwrite ' + home + '/Desktop/' + name2 + ' ' + home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
		elif 'flac' in format:
			name3 += 'flac'
			cmd += 'flac -f -8 ' + home + '/Desktop/' + name2 + ' -o ' + home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
	elif 'audaud' in contype:
		if oldext != 'wav':
			cmd = 'mplayer -vc null -vo null -af resample=44100 -srate 44100 -ao pcm:fast:file=' + home + '/Desktop/' + name2 + ' ' + filename + ' 2>' + home + '/errors.txt && '
		if 'mp3' in format:
			name3 += 'mp3'
			cmd += 'lame -b 192 ' + home + '/Desktop/' + name2 + ' ' + home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
		elif 'aac' in format:
			name3 += 'm4a'
			cmd += 'faac -w -s -b 192 -o ' + home + '/Desktop/' + name3 + ' ' + home + '/Desktop/' + name2 + ' 2>>' + home + '/errors.txt'
		elif 'ogg' in format:
			name3 += 'ogg'
			cmd += 'oggenc -q 5 ' + home + '/Desktop/' + name2 + ' -o ' + home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
		elif 'mpc' in format:
			name3 += 'mpc'
			cmd += 'mppenc --overwrite ' + home + '/Desktop/' + name2 + ' ' + home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
		elif 'flac' in format:
			name3 += 'flac'
			cmd += 'flac -f -8 ' + home + '/Desktop/' + name2 + ' -o ' + home + '/Desktop/' + name3 + ' 2>>' + home + '/errors.txt'
	cmd += ' && rm ' + home + '/Desktop/' + name2
	self.progress(cmd)

    def callback(self, widget, contype, data=None):
	if "ON" in (data, ("OFF","ON")[widget.get_active()]):
		if 'audaud' in contype:
			self.aaformat.set_text(data)
		elif 'audvid' in contype:		
			self.avformat.set_text(data)

    def __init__(self):

	aaformat = gtk.Entry() 
	aaformat.set_text('mp3')
	self.aaformat = aaformat

	avformat = gtk.Entry()
	avformat.set_text('mp3')
	self.avformat = avformat

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.window.set_title("MMMC - Mark's Multi Media Converter")
	self.window.set_icon_from_file(file_name)
        self.window.connect("delete_event", gtk.main_quit)
        self.window.set_border_width(10)

        table = gtk.Table(3,6)
        self.window.add(table)

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(self.notebook, 0,6,0,1)
        self.notebook.show()
	self.show_tabs = True
	self.show_border = True

        bufferf = "Mark's Multi Media Converter"
        bufferl = "MMMC"

        self.frame = gtk.Frame(bufferf)
        self.frame.set_border_width(25)
        self.frame.set_size_request(900, 450)
        pixbuf = gtk.gdk.pixbuf_new_from_file(file_name)
        pixmap, mask = pixbuf.render_pixmap_and_mask()
      	image = gtk.Image()
      	image.set_from_pixmap(pixmap, mask)
	bigbox = gtk.VBox()
	vbox = gtk.VBox()
	hbox=gtk.HBox()
	hbox.pack_start(image)
	bigbox.pack_start(vbox)
	bigbox.pack_start(hbox)
	self.frame.add(bigbox)        
	self.frame.show_all()
        label = gtk.Label(bufferl)
        self.notebook.append_page(self.frame, label)

	bufferf = "Mark's Multi Media Converter"
        bufferl = "Audio From Video"
	self.frame = gtk.Frame(bufferf)
        self.frame.set_border_width(25)
        self.frame.set_size_request(900, 450)
        button = gtk.Button("Choose Video File")
	contype='audvid'
	button.connect("clicked", self.file_select, contype)
	filename = ""	
	button2 = gtk.Button("Extract and Convert")
	button2.connect("clicked", self.convert, contype)
	self.audvidentry = gtk.Entry()

	bigbox = gtk.VBox()
	hbox = gtk.HBox()
	hbox2 = gtk.HBox()
	hbox.pack_start(self.audvidentry, padding=10)
	hbox2.pack_start(button, padding=10)
	hbox2.pack_start(button2, padding=10)
	bigbox.pack_start(hbox, padding=10)
	bigbox.pack_start(hbox2, padding=10)

	self.bradio(contype)
	bigbox.pack_start(self.box0)
	self.frame.add(bigbox)
        self.frame.show_all()

        label = gtk.Label(bufferl)
        self.notebook.append_page(self.frame, label)

	bufferf = "Mark's Multi Media Converter"
        bufferl = "Audio to Audio"

	self.frame = gtk.Frame(bufferf)
        self.frame.set_border_width(25)
        self.frame.set_size_request(900, 450)
	contype='audaud'
        button = gtk.Button("Click To Choose Audio File")
	button.connect("clicked", self.file_select, contype)
	button2 = gtk.Button("Convert")
	button2.connect("clicked", self.convert, contype)
	self.audaudentry = gtk.Entry()

	bigbox = gtk.VBox()
	vbox = gtk.VBox()
	vbox.pack_start(self.audaudentry, padding = 10)
	vbox.pack_start(button, padding = 10)
	hbox = gtk.HBox()
	hbox.pack_start(vbox, padding = 10)
	hbox.pack_start(button2, padding = 10)
	bigbox.pack_start(hbox, padding = 10)
	self.bradio(contype)
	bigbox.pack_start(self.box0)
	self.frame.add(bigbox)
        self.frame.show_all()

        label = gtk.Label(bufferl)
        self.notebook.append_page(self.frame, label)

	bufferf = "Mark's Multi Media Converter"
        bufferl = "Video to Video"

        self.frame = gtk.Frame(bufferf)
        self.frame.set_border_width(25)
        self.frame.set_size_request(900, 450)
	contype = 'vidvid'
	box = gtk.HBox()
	button = gtk.Button("Click To Choose Video File")
	button.connect("clicked", self.file_select, contype)
	self.vidfile = gtk.Entry()
	self.vidfile.set_width_chars(50)
	label1 = gtk.Label("File:")
	box.pack_start(label1, expand=False, padding = 10)
	box.pack_start(self.vidfile, padding = 10)
	box.pack_start(button, padding = 10)
	containerbox = gtk.HBox()
	containerlabel = gtk.Label("Container: ")
	vformatlabel = gtk.Label("Video Codec: ")
	aformatlabel = gtk.Label("Audio Codec: ")
	container = gtk.combo_box_new_text()
	container.append_text("Select Format:")
	container.append_text("3gp")
	container.append_text("avi")
	container.append_text("asf")
	container.append_text("flv")
	container.append_text("m4v")
	container.append_text("mov")
	container.append_text("mp4")
	container.append_text("mkv")
	container.append_text("ogv")
	container.append_text("psp")
	container.append_text("rmv")
	container.append_text("swf")
	container.append_text("wmv")
	container.set_active(0)
	self.container = container
	self.container.show()
	self.container.connect('changed', self.container_update)
	containerbox.pack_start(containerlabel)
	containerbox.pack_start(self.container)
	self.vformat = gtk.combo_box_new_text()
	self.vformat.show()
	self.aformat = gtk.combo_box_new_text()
	self.aformat.show()
	self.aformat.connect('changed', self.aset)
	containerbox.pack_start(vformatlabel, padding = 10)
	containerbox.pack_start(self.vformat, padding = 10)
	containerbox.pack_start(aformatlabel, padding = 10)
	containerbox.pack_start(self.aformat, padding = 10)
	param1box = gtk.HBox()
	scalelabel = gtk.Label("Video Scale:")
	vbrlabel = gtk.Label("Video Bitrate:")
	abrlabel = gtk.Label("Audo Bitrate:")
	self.scale = gtk.combo_box_new_text()
	self.scale.show
	self.vbr = gtk.combo_box_new_text()
	self.vbr.show
	self.abr = gtk.combo_box_new_text()
	self.abr.show
	param1box.pack_start(scalelabel, padding = 10)
	param1box.pack_start(self.scale, padding = 10)
	param1box.pack_start(vbrlabel, padding = 10)
	param1box.pack_start(self.vbr, padding = 10)
	param1box.pack_start(abrlabel, padding = 10)
	param1box.pack_start(self.abr, padding = 10)
	param1box.show_all()
	box.show_all()
	containerbox.show_all()
	convertbox = gtk.HBox()
	convertbutton = gtk.Button("Convert")
	convertbutton.connect("clicked", self.vidconvert)
	convertbox.pack_start(convertbutton, padding = 10)
	convertbox.show_all()		
	mainbox = gtk.VBox()
	mainbox.pack_start(box, padding = 10)
	mainbox.pack_start(containerbox, padding = 10)
	mainbox.pack_start(param1box, padding = 50)
	mainbox.pack_start(convertbox, padding = 10)
	mainbox.show_all()

	self.frame.add(mainbox)
        self.frame.show()

        label = gtk.Label(bufferl)
        self.notebook.append_page(self.frame, label)

	bufferf = "Mark's Multi Media Converter"
        bufferl = "Merge Video"

        self.frame = gtk.Frame(bufferf)
        self.frame.set_border_width(25)
        self.frame.set_size_request(900, 450)
	
	bigbox = gtk.VBox()
	bigbox.set_border_width(15)
	smallbox = gtk.HBox()
	smallbox.set_border_width(25)
	sw = gtk.ScrolledWindow()
	sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	entrymerge = gtk.TextView()
	entrymerge.set_editable(False)
	self.textbuffer = entrymerge.get_buffer()
	sw.add(entrymerge)
	sw.show()
	entrymerge.show()
	bigbox.pack_start(sw, padding=10)
	bigbox.show_all()
	entrymerge.set_buffer(self.textbuffer)
	button = gtk.Button("Click To Add Video to List")
	contype = 'merge'
	button.connect("clicked", self.file_select, contype)
	button2 = gtk.Button("Clear Selections")
	button2.connect("clicked", self.clear)
	button3 = gtk.Button("Merge Video Files")
	button3.connect("clicked", self.filechoose)
	smallbox.pack_start(button)
	smallbox.pack_start(button2)
	smallbox.pack_start(button3)
	smallbox.show_all()
	bigbox.pack_start(smallbox)
	self.frame.add(bigbox)
        self.frame.show_all()

        label = gtk.Label(bufferl)
        self.notebook.append_page(self.frame, label)

	bufferf = "Mark's Multi Media Converter"
        bufferl = "Split Video"

        self.frame = gtk.Frame(bufferf)
        self.frame.set_border_width(25)
        self.frame.set_size_request(900, 450)
	contype='split'
	bigbox = gtk.VBox()
	box = gtk.HBox()
	box2 = gtk.HBox()
	button = gtk.Button("Click To Choose Video File")
	button.connect("clicked", self.file_select, contype)
	self.splitentry = gtk.Entry()
	self.splitentry.set_width_chars(50)
	label1 = gtk.Label("File:")
	box.pack_start(label1, expand=False, padding = 10)
	box.pack_start(self.splitentry)
	box.pack_start(button, padding = 10)
	box.show_all()
	hourbox = gtk.HBox()
	minutebox = gtk.HBox()
	splitbox = gtk.HBox()
	vertbox = gtk.HBox()
	label = gtk.Label("Enter hours:")
	self.entry2 = gtk.Entry()
	self.entry2.insert_text('00')
	self.entry2.set_width_chars(3)
	label2 = gtk.Label("Enter minutes:")
	self.entry3 = gtk.Entry()
	self.entry3.insert_text('00')
	self.entry3.set_width_chars(3)
	label.show()
	label2.show()
	button2 = gtk.Button("                                             Split  Video                                                ")
	button2.connect("clicked", self.split)
	splitbox.pack_start(button2, padding = 10)
	splitbox.show_all()
	hourbox.pack_start(label, expand = False)
	hourbox.pack_start(self.entry2, padding = 10)
	minutebox.pack_start(label2, expand = False)
	minutebox.pack_start(self.entry3, padding = 10)
	vertbox.pack_start(hourbox)
	vertbox.pack_start(minutebox, padding = 10)
	hourbox.show_all()
	minutebox.show_all()
	box2.pack_start(vertbox, padding = 10)
	box2.pack_start(splitbox)
	box2.show_all()
	bigbox.pack_start(box, padding = 10)
	bigbox.pack_start(box2, padding = 10)
	bigbox.show_all()
	self.frame.add(bigbox)
        self.frame.show_all()

        label = gtk.Label(bufferl)
        self.notebook.append_page(self.frame, label)

        button = gtk.Button("close")
        button.connect("clicked", gtk.main_quit)
	button.set_border_width(25)
        table.attach(button, 0,1,1,2)
        button.show()
        table.show()
        self.window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    MMMC()
    main()
