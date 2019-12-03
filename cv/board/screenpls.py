import pyscreenshot as ig
import uuid

if __name__ == "__main__":
	#random file name
	savePath = str(uuid.uuid4()) + ".png"

	#get screenshopt and save temporarily
	img = ig.grab()
	img.save(savePath)
