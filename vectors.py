#! /usr/bin/env python

####################################
# Python Vector Manipulation Shell #
#      Lyell Read | 6/15/2018      #
####################################

from cmd import Cmd
import math

data_file = "data.txt"

class VecPrompt (Cmd):

	def do_input(self,args):
		"""  Func.: Lets you input vector(s) in x- and y- components, mangitude and angle (deg | rad) into the program\n  Usage: + input (xy | deg | rad) (x1 y1 x2 y2 ... | mag1 deg1 mag2 deg2 ... | mag1 rad1 mag2 rad2 ...) \n  Notes: Input checked for even number of args.\n         Enter 0 instead of leaving an entry blank."""
		if len(args) == 0 or not (len(args.split())-1)%2 == 0 or not args.split()[0] in ['xy','deg','rad']:
			print(args.split())
			print("Invalid Answer; Breaking")
		else:
			print("---->Passed with arglist: " + args)

			arglist=args.split()
			type = arglist[0]
			arglist.remove(arglist[0])
			arglist_float = [float(arg) for arg in arglist]

			for pair in range (0,len(arglist_float)/2):
				pair_vec = arglist_float [0:2]
				if type == 'xy':
					print ("------>Adding Vector with X component " + str(pair_vec[0]) + " and Y component " + str(pair_vec[1]))
					# MUST ADD
				else:
					print ("------>Converting Vector with Magintude " + str(pair_vec[0]) + " and angle " + str(pair_vec[1]))
					pair_vec= VecPrompt.convert_to_xy(self, pair_vec, type)
					print ("------>Adding Vector with X component " + str(pair_vec[0]) + " and Y component " + str(pair_vec[1]))
				print(pair_vec)
				arglist_float=[arg for arg in arglist_float[2:]]

	def convert_to_xy (self, pair, type):
		if not len(pair) == 2:
			print ("Error Breaking!")
		return_pair = []
		if type == 'rad' :
			return_pair = [pair[0]*math.cos(pair[1]),pair[0]*math.sin(pair[1])]
			return return_pair
		elif type == 'deg' :
			return_pair = [pair[0]*math.cos(math.radians(pair[1])),pair[0]*math.sin(math.radians(pair[1]))]
			return return_pair
		else:
			print("Unknown Type; Error; Breaking")



	def do_quit(self, args):
		"""  Func.: Quits the program\n  Usage: + quit \n  Notes: No arguments needed"""
		print ("Quitting Immediately")
		raise SystemExit


if __name__ == "__main__":
	prompt = VecPrompt()
	prompt.prompt = '+ '
	prompt.cmdloop('Entering the Vectropy Shell...')
