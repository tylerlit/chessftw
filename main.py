from cv.board import annotate, screenshot
from dev import dev_functions
import argparse

if __name__ == '__main__':
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-a", "--annotate", action="store_true",
						help="annotate unlabelled images")
	ap.add_argument("-s", "--screenshot", action="store_true",
						help="take screenshot of main screen (pls screen chess game)")
	ap.add_argument("-db", "--deleteBoard", nargs="*", 
						help="delete board image from S3 and chess.board. uses chess.board ID value")
	ap.add_argument("-sb", "--showBoard", nargs = 2,
						help="""<directory> <# of images to download>

						takes in a directory and dowloads all files from s3.""")
	ap.add_argument("-rbl", "--resetBoardLocks", action="store_true",
						help="Resets locked colums to 0 in chess.board")
	args = ap.parse_args()

	if args.deleteBoard != None:
		for id in args.deleteBoard:
			dev_functions.deleteBoardImage(id)
			print(id + ' deleted.')

	if args.showBoard != None:
		dev_functions.dowloadBoards(args.showBoard[0], args.showBoard[1])

	if args.annotate:
		annotate.run()

	if args.screenshot:
		screenshot.run()

	if args.resetBoardLocks:
		dev_functions.resetBoardLocks()