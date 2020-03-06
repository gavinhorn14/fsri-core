#################################################################
# Author: Zevotek												#
# Purpose: Extract images from a video at particular timesteps	#
# Use: Fill in the values under the main program header to set 	#
# 		variables for image collection from a video. If			#
# 		build_latex is true a figure.tex file will be created 	#
# 		with a subfigure for each image. The default is 3 		#
# 		images across but can be altered in the options 		#
# Revision Date: 3-4-2020										#
#################################################################

import cv2

def get_images(vid, cap_times, output, latex_path='', write_latex = False, top=0, left=0, bottom=0, right=0, latex_row=3):

# Variables:
#	Required:
# 		vid - Path to video file.
# 		cap_times - array of times to capture in seconds from start of video
# 		output - (str) path to where the image files should be located
# 	Optional:
# 		latex_path - (str) relative path from latex file to images
#   	write_latex - (bol) Default=False, determines whether to develop latex file.
# 		top - (float) percentage to crop from top of frame as a fraction of the total height
# 		bottom -  (float) percentage to crop from the bottom of frame as a fraction of the total height
# 		left - (float) percentage to crop from left of frame as a fraction of the total width
# 		right - (float) percentage to crop from right of frame as a fraction of the total width
	
	#Load video
	vid = cv2.VideoCapture(vid)

	#Get frame rate
	frame_rate = vid.get(cv2.CAP_PROP_FPS)

	#Loop through capture times to grab images
	for t in cap_times:

		#Set video to frame of interest
		vid.set(cv2.CAP_PROP_POS_FRAMES, t*frame_rate)

		#Read the frame
		ret, frame = vid.read()

		if ret:
			#Get height h, width w, and c channels (colors) for frame
			h, w, c = frame.shape

			#Crop frame using top, left, right, bottom
			frame = frame[0+int(h*top):h-int(h*bottom),0+int(w*left):w-int(w*right)].copy()

			#Write image to local directory with the 
			cv2.imwrite(output + str(t) + '.jpg', frame) 

		else:
			print ('No Frame at ' + str(t) + 'seconds. Video length is only ' + str(int(vid.get(CV_CAP_PROP_FRAME_COUNT)/frame_rate)) + 'seconds long.')

	vid.release()
	cv2.destroyAllWindows()

	#If write latex is true, construct a figures.tex file in the image output directory with each image as a subfigure
	if write_latex:
		file = open('figures.tex', 'w')

		begin_fig = ['\\begin{figure}[H]\n', '\t\\centering\n'] 
		begin_subfig = ['\t\\begin{subfigure}{'+str(round(1/latex_row,2)-0.01)+'\\textwidth}\n', '\t\t\\centering\n']

		end_sub_fig = ['\t\\end{subfigure}\n']
		end_fig = ['\t\\caption[]{}\n', '\t\\label{}\n', '\\end{figure}\n']

		for l in begin_fig:
			file.write(l)

		for image in cap_times:
			for l in begin_subfig:
				file.write(l)

			line = '\t\t\\includegraphics[width=\\textwidth]{' + latex_path + str(image) + '}\n' 
			file.write(line)

			line = '\t\t\\caption{' + str(image) + ' seconds}\n'
			file.write(line)

			for l in end_sub_fig:
			 	file.write(l)

		for l in end_fig:
			file.write(l)

		file.close()

################################
################################
######### Main Program 	########
################################
################################

# Required Items 
####################

#Path to video file
video_file = ''

#Name you would like all images to start with to image 
name = 'Image_'

#Path to location you would like images stored (default is current directory)
output_location = ''

#Times to capture in secionds
times = [0,10,20,30,40,50,60]

# Options
####################

#If you would like a latex file developed set build_latex to True
build_latex = False

#Path where latex file can finde images for figure reference.
relative_latex_path = '../05_Figures/'

#Number of images in a row
row_images = 3

#Fraction of image to crop off ie. 0.5 crops half the image, 0.2 takes the top, left, right or bottom 20%
top_crop = 0
left_crop = 0
bottom_crop = 0
right_crop = 0

print ('Exporting frame from ' + video_file)

get_images(video_file, times, output_location+name, relative_latex_path+name, build_latex, top_crop, left_crop, bottom_crop, right_crop, row_images)

print ('Export complete')