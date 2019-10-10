import pyscreenshot as ig
import uuid

if __name == "__main__":
	img = ig.grab()
	img.save(str(uuid.uuid4()) + ".png")

#img.show()