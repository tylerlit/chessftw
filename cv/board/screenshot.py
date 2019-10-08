import pyscreenshot as ig
import uuid

img = ig.grab()
img.save(str(uuid.uuid4()) + ".png")

#img.show()