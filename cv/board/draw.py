import cv2 

# now let's initialize the list of reference point 
ref_point = [] 
crop = False

def shape_selection(event, x, y, flags, param): 
	# grab references to the global variables 
	global ref_point, crop 

	# if the left mouse button was clicked, record the starting 
	# (x, y) coordinates and indicate that cropping is being performed 
	if event == cv2.EVENT_LBUTTONDOWN: 
		ref_point = [(x, y)] 

	# check to see if the left mouse button was released 
	elif event == cv2.EVENT_LBUTTONUP: 
		# record the ending (x, y) coordinates and indicate that 
		# the cropping operation is finished 
		ref_point.append((x, y)) 

		# draw a rectangle around the region of interest 
		cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2) 
		cv2.imshow("image", image) 

def draw(img):

	global image, clone

	# load the image, clone it, and setup the mouse callback function 
	image = cv2.imread(img)
	clone = image.copy() 
	cv2.namedWindow("image") 
	cv2.setMouseCallback("image", shape_selection) 


	while True: 

		cv2.imshow("image", image) 
		key = cv2.waitKey(0) & 0xFF

		# reset the window 
		if key == ord("r"): 
			image = clone.copy() 

		elif key == ord("c"): 
			if len(ref_point) == 2: 
				crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]

				cv2.imshow("crop_img", crop_img)
				if cv2.waitKey(0) & 0xFF == ord("c"):
					break
				else:
					cv2.destroyWindow("crop_img")
					image = clone.copy()


	# close all open windows 
	cv2.destroyAllWindows()

	return crop_img, ref_point