#! /usr/bin/env python

#full verbosity
#input check for spaces
#Maths

####################################
# Python Vector Manipulation Shell #
#      Lyell Read | 6/15/2018      #
####################################

from cmd import Cmd
import math

version = "1.0.3"
data_file = "data.txt" #replace with path to file if it is somewhere else...

class VecPrompt (Cmd):


## Basic Manipulation Tools ##


	def do_input(self,args):
		"""\n  Input Help Entry\n  ================\n  Func.: Lets you input vector(s) in x- and y- components, mangitude and angle (deg | rad) into the program\n  Usage: + input (xy | deg | rad) (x1 y1 x2 y2 ... | mag1 deg1 mag2 deg2 ... | mag1 rad1 mag2 rad2 ...) \n  Notes: Input checked for even number of args.\n         Enter 0 instead of leaving an entry blank.\n"""

		output=open(data_file, "a+")
		if len(args) == 0 or not (len(args.split(" "))-1)%2 == 0 or not args.split(" ")[0] in ['xy','deg','rad']:
			print("-err-> Too few or offset args or improper type")
			return 0
		else:
			arglist=args.split(" ")
			type = arglist[0]
			arglist.remove(arglist[0])
			arglist_float = [float(arg) for arg in arglist]
			for pair in range (0,len(arglist_float)/2):
				pair_vec = arglist_float [0:2]
				if type != 'xy':
					print("-----> Converting both vectors to XY format")
					#print ("-----> Converting Vector with Magintude " + str(pair_vec[0]) + " and angle " + str(pair_vec[1]) + " " + type)
					pair_vec= VecPrompt.convert_to_xy(self, pair_vec, type)
				#print ("-----> Adding Vector with X component " + str(pair_vec[0]) + " and Y component " + str(pair_vec[1]))

				#Write to File
				output.write(str(pair_vec[0]) + " " + str(pair_vec[1])+"\n")
				arglist_float=[arg for arg in arglist_float[2:]]

		print ("-----> Input Finished!")
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
			print("-err-> Unknown Type; Error; Breaking")

	def do_clear (self, args):
		"""\n  Clear Help Entry\n  ================\n  Func.: Clears stored vectors\n  Usage: + clear\n  Notes: Clears all vectors. Permanently ;)\n"""

		VecPrompt.do_print(self,0)
		#Verify Certainty!
		verify = raw_input("-ver-> Are you sure you want to clear vectors printed above? (y/n):")
		if verify.lower() == "y":
			print("-----> Clearing file: " + str(data_file))
			open(data_file, 'w').close() # clears file
			print("-----> File cleared. Finished.")
		else:
			print ("-----> Not clearing file. Finished.")

	def do_print (self, args):
		"""\n  Print Help Entry\n  ================\n  Func.: Prints all vectors in storage.\n  Usage: + print\n  Notes: None, sorry!\n"""
		source=open(data_file, "r")
		source_data = source.readlines()
		for line_num in range (0,len(source_data)):
			print ("-----> [" + str(line_num) + "] : " + str(source_data[line_num].split()[0]) + ", " + str(source_data[line_num].split()[1]))

	def do_remove (self, args):
		# define help menu. ~pretty standard, really~
		"""\n  Remove Help Entry\n  =================\n  Func.: Removes a vector from storage.\n  Usage: + remove [n1 n2 n3...]\n  Notes: If you do not specify line numbers (n1 n2 ...) you can choose interacively\n         The line number input starts at line 0 and specifying the lines as parameters is used internally.\n         If mutiple identical vectors exist and you choose to remove one, it will get all of 'em'\n"""

		data = open(data_file, "r+")
		source_data = data.readlines()

		#Build Data Validation list to check input against.
		data_validation = []
		for line in range (0,len(source_data)):
			data_validation.append(str(line))
		# if there are no args, then the user is using remove() to remove their choice, thus input needed.
		if len(args) == 0:
			VecPrompt.do_print(self,0) #Print out all the vectors in storage
			#Build an argument list from the input of the user
			arglist = raw_input("-----> Choose which to remove. Split with spaces: ").split(" ")
			for arg in arglist:
				if not arg in data_validation:
					print ("-err-> Validation failed on user-entered argument: " + arg + " --> Breaking, nothing removed.")
					return 0
					#Break if the arg check failsself.
			#Otherwise, if the arglist completes, set it to be the definitive one
			args = arglist
		else:
			#This case is where another fxn called remove() and we're just getting the args from that
			args=args.split(" ")

		#Reverse sort that list of args to take the largest first (thus it will not change the pos of the next item to be removed...)_
		args.sort(key=int, reverse=True)

		remove_list = []
		data.close()

		for arg in args:
			remove_list.append(source_data[int(arg)])

			for line in source_data:
				if line in remove_list:
					source_data.remove(line)
					data = open(data_file, "w")
					for line in source_data:
						data.write(line)
					data.close()
		print("-----> Remove Finished!")


## Math Tools ##


	def do_inverse (self, args):
		"""\n  Inverse Help Entry\n  ==================\n  Func.: Takes the inverse of a vector. This is the equivalent of rotating the vector by 180 degrees.\n  Usage: + inverse\n  Notes: none\n"""

		if len(args) == 0:
			VecPrompt.do_print(self,0)
			inverses = raw_input("-----> Enter all you wish to flip, separated by spaces: ").split(' ')
		else:
			inverses=args.split(" ")

		data = open(data_file, "r+")
		source_data = data.readlines()

		data_validation = []
		for line in range (0,len(source_data)):
			data_validation.append(str(line))

		for arg in inverses:

			if not arg in data_validation:
				print ("-err-> Input out of range or invalid. Nothing inversed. Breaking!")
				return 0

		for x in range (0,len(inverses)):

			VecPrompt.do_remove(self,str(inverses[x]))

			temp_vec = source_data[int(inverses[x])]
			inversed_vec =[]
			for component in temp_vec.split(" "):
				inversed_vec.append(-1 * float(component))
			VecPrompt.do_input(self,"xy " + str(inversed_vec[0]) + " " + str(inversed_vec[1]))
		print ("-----> Inverse Finished")

## Exiting Tools ##


	def do_quit(self, args):
		"""\n  Quit Help Entry\n  ===============\n  Func.: Quits the program\n  Usage: + quit \n  Notes: No arguments needed\n         Same as `exit`/n"""
		print ("Quitting Immediately")
		raise SystemExit

	def do_exit(self, args):
		"""\n  Exit Help Entry\n  ===============\n  Func.: Quits the program\n  Usage: + exit \n  Notes: No arguments needed\n         Same as `quit`\n"""
		print ("Quitting Immediately")
		raise SystemExit


## Program Start ##


if __name__ == "__main__":
	prompt = VecPrompt()
	prompt.prompt = '+ '
	prompt.cmdloop('Entering the Vectropy ' + version + ' Shell... Enter `+ quit` to quit.')
