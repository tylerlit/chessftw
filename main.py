from cv.board import annotate, screenshot
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--annotate", action="store_true",
					help="annotate unlabelled images")
ap.add_argument("-s", "--screenshot", action="store_true",
					help="take screenshot of main screen (pls screen chess game)")
args = ap.parse_args()


if args.annotate:
	annotate.run()

if args.screenshot:
	screenshot.run()