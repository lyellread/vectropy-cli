#! /usr/bin/env python

####################################
# Python Vector Manipulation Shell #
#      Lyell Read | 6/15/2018      #
####################################

from cmd import Cmd
import math

version = "1.0.1"
data_file = "data.txt" #replace with path to file if it is somewhere else...

class VecPrompt (Cmd):

	def do_input(self,args):
		"""  Func.: Lets you input vector(s) in x- and y- components, mangitude and angle (deg | rad) into the program\n  Usage: + input (xy | deg | rad) (x1 y1 x2 y2 ... | mag1 deg1 mag2 deg2 ... | mag1 rad1 mag2 rad2 ...) \n  Notes: Input checked for even number of args.\n         Enter 0 instead of leaving an entry blank."""
		print("-----> Started!")
		output=open(data_file, "a+")
		if len(args) == 0 or not (len(args.split())-1)%2 == 0 or not args.split()[0] in ['xy','deg','rad']:
			print("-err-> Invalid Answer; Breaking")
		else:
			print("-----> Passed with arglist: " + args)

			arglist=args.split()
			type = arglist[0]
			arglist.remove(arglist[0])
			arglist_float = [float(arg) for arg in arglist]
			for pair in range (0,len(arglist_float)/2):
				pair_vec = arglist_float [0:2]
				if type != 'xy':
					print ("-----> Converting Vector with Magintude " + str(pair_vec[0]) + " and angle " + str(pair_vec[1]) + " " + type)
					pair_vec= VecPrompt.convert_to_xy(self, pair_vec, type)
				print ("-----> Adding Vector with X component " + str(pair_vec[0]) + " and Y component " + str(pair_vec[1]))

				#Write to File
				output.write(str(pair_vec[0]) + " " + str(pair_vec[1])+"\n")

				arglist_float=[arg for arg in arglist_float[2:]]

		print ("-----> Finished!")
		output.close()

	def convert_to_xy (self, pair, type):
		if not len(pair) == 2:
			print ("-err-> Pair Length Error Breaking!")
		return_pair = []
		if type == 'rad' :
			return_pair = [pair[0]*math.cos(pair[1]),pair[0]*math.sin(pair[1])]
			return return_pair
		elif type == 'deg' :
			return_pair = [pair[0]*math.cos(math.radians(pair[1])),pair[0]*math.sin(math.radians(pair[1]))]
			return return_pair
		else:
			print("-err->Unknown Type; Error; Breaking")

	def do_clear (self, args):
		"""  Func.: Clears stored vectorsm\n  Usage: + clear\n  Notes: Clears all vectors. Permanently ;)"""
		#Verify Certainty!
		VecPrompt.do_print(self,0)
		verify = raw_input("-ver-> Are you sure you want to clear vectors printed above? (y/n):")
		if verify.lower() == "y":
			print("-----> Clearing file: " + str(data_file))
			open(data_file, 'w').close() # clears file
			print("-----> File cleared. Finished.")
		else:
			print ("-----> Not clearing file. Finished.")

	def do_print (self, args):
		source=open(data_file, "r")
		source_data = source.readlines()
		for line_num in range (0,len(source_data)):
			print ("-----> [" + str(line_num+1) + "] : " + str(source_data[line_num].split()[0]) + ", " + str(source_data[line_num].split()[1]))

	def do_quit(self, args):
		"""  Func.: Quits the program\n  Usage: + quit \n  Notes: No arguments needed"""
		print ("Quitting Immediately")
		raise SystemExit

	def do_exit(self, args):
		"""  Func.: Quits the program\n  Usage: + quit \n  Notes: No arguments needed"""
		print ("Quitting Immediately")
		raise SystemExit
if __name__ == "__main__":
	prompt = VecPrompt()
	prompt.prompt = '+ '
	prompt.cmdloop('Entering the Vectropy ' + version + ' Shell... Enter `+ quit` to quit.')
