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

version = "2.0.2" #testing 3d branch
data_file = "data.txt" #replace with path to file if it is somewhere else...

class VecPrompt (Cmd):


## Basic Manipulation Tools ##


	def do_input(self,args):
		"""\n  Input Help Entry\n  ================\n  Func.: Lets you input vector(s) into the program\n  Usage: + input xyz x1 y1 z1 x2 y2 z2 ...\n        + input deg mag1 amgle1 mag2 angle2\n         + input rad mag1 angle1 mag2 angle2\n  Notes: Input checked for appropriate number of arguments, add a 0 for z in xyz to have 2d vectors.\n         Enter 0 instead of leaving an entry blank.\n"""

		output=open(data_file, "a+")
		arguments = args.split(" ")

		if len(aruments) < 3: # 0,1,2
			print ("-err-> Too few arguments provided.")
			return 0

		if arguments[0] not in ['xyz','deg','rad']:
			print ("-err-> Improper type entered.")
			return 0

		if arguments[0] in ['deg','rad'] and not (len(arguments)-1)%2 == 0: #checks for odd number of arguments if we are working with DEG or RAD
			print("-err-> Wrong amount of arguments for selected mode.")
			return 0

		if arguments[0] == 'xyz' and not (len(arguments)-1)%3 == 0: #checks for multiple of three number of arguments if we are working with XYZ
			print("-err-> Wrong amount of arguments for selected mode.")
			return 0

		type = arguments[0]
		arguments.remove(arguments[0])
		arguments_float = [float(arg) for arg in arguments]

		if type != "xyz":
			for pair in range (0,len(arguments_float)/2):
				pair_vec = arguments_float [0:2]
				print("-----> Converting vector to XYZ format")
				#print ("-----> Converting Vector with Magintude " + str(pair_vec[0]) + " and angle " + str(pair_vec[1]) + " " + type)
				pair_vec= VecPrompt.convert_to_xy(self, pair_vec, type)
				#print ("-----> Adding Vector with X component " + str(pair_vec[0]) + " and Y component " + str(pair_vec[1]))

				#Write to File
				output.write(str(pair_vec[0]) + " " + str(pair_vec[1])+" 0\n") #" 0" at the end is to set a zero valued Z component - the only one possible with the available info.
				arguments_float=arguments_float[2:] #redefine the arguments to be all but the first two, repeat.

			print ("-----> Input Finished!")
			output.close()

		else: #xyz
			for trio in range (0,len(arguments_float)/3):
				trio=arguments_float[0:3]
				print ("-----> Adding Vector with X component " + str(trio[0]) + " and Y component " + str(trio[1]) + " and Z component " + str(trio[2]))
				output.write(str(trio[0]) + " " + str(trio[1]) + " " + str(trio[2]) + "\n")
				arguments_float=arguments_float[3]:]


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
		#Verify User Certainty!
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
			print ("-----> [" + str(line_num) + "] : " + str(source_data[line_num].split()[0]) + ", " + str(source_data[line_num].split()[1]) + ", " str(source_data[line_num].split()[2]))

	def do_remove (self, args):
		# define help menu. ~pretty standard, really~
		"""\n  Remove Help Entry\n  =================\n  Func.: Removes a vector from storage.\n  Usage: + remove [n1 n2 n3...]\n  Notes: If you do not specify line numbers (n1 n2 ...) you can choose interacively\n         The line number input starts at line 0 and specifying the lines as parameters is used internally.\n"""

		data = open(data_file, "r+")
		source_data = data.readlines()

		#Build Data Validation list to check input against. TODO: Use list comp to make neat!
		data_validation = []
		for line in range (0,len(source_data)):
			data_validation.append(str(line))

		# if there are no args, then the user is using remove() to remove their choice, thus input needed.
		if len(args) == 0:
			VecPrompt.do_print(self,0) #Print out all the vectors in storage

			#Build an argument list from the input of the user
			arguments = raw_input("-----> Choose which to remove. Split with spaces: ").split(" ")
			for arg in arguments:
				if not arg in data_validation:
					print ("-err-> Validation failed on user-entered argument: " + arg + " --> Breaking, nothing removed.")
					return 0 #Break if the arg check failsself.

			#Otherwise, if the arguments completes, set it to be the definitive one
			args = arguments

		else:
			#This case is where another fxn called remove() and we're just getting the args from that - we trust that function to be 'spot on chaps.'
			args=args.split(" ")

		#Reverse sort that list of args to take the largest first (thus it will not change the pos of the next item to be removed...) (guess who got to find that out the hard way xD)
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
					break
		print("-----> Remove Finished!")


## Math Tools ##


	def do_add (self,args):
		"""\n  Add Help Menu\n  =============\n  Func.: Adds n vectors together\n  Usage: + add [store output? (Y|N)] [remove inputs? (Y|N)] n1 n2 ... \n  Notes: To get the same function as subtract, inverse, then add.\n         Store Output: Y: adds new vector for resultant; N: Prints the resultant, does not save.\n         Remove Inputs: Y: removes all input vectors (n1, n2 ...); N: Does not touch input Vectors.\n"""

		args=args.split(" ")

		if len(args)<4:
			print("-err-> Too few arguments entered. Please retry. Breaking!")
			return 0

		if args[0].upper() not in ('Y','N') or args[1].upper() not in ('Y','N'):
			print("-err-> Invalid arguments parsed (first two need to be 'Y' or 'N')")
			return 0

		#Build Data Validation list to check input against.
		data = open(data_file, "r+")
		source_data = data.readlines()

		data_validation = []
		for line in range (0,len(source_data)):
			data_validation.append(str(line))

		inputs = []

		for arg in args[2:len(args)]:
			if not arg in data_validation:
				print ("-err-> Invalid vector index entered: " + arg)
				return 0
			else:
				inputs.append(source_data[int(arg)].split())

		final_x = 0
		final_y = 0
		final_z = 0

		#here I could see doing something with sets, tuples or list additions
		for vector in inputs:
			final_x += float(vector[0])
			final_y += float(vector[1])
			final_y += float(vector[2])

		print("-res-> Resultant: X: " + str(final_x) + "; Y: " + str(final_y)+ "; Z: " + str(final_z))

		if args[0].upper() == "Y": # Store the output to file, using the already defined input function
			VecPrompt.do_input(self, "xyz " + str(final_x) + " " + str(final_y) + " " + str(final_z))

		if args[1].upper() == "Y": # Remove the input vectors
			for arg in args[2:len(args)]:
				VecPrompt.do_remove(self,arg)

		print("-----> Add Function Finished!")



	def do_inverse (self, args):
		"""\n  Inverse Help Entry\n  ==================\n  Func.: Takes the inverse of a vector. This is the equivalent of creating a new vector with an equal magnitude and opposite direction to the first vector.\n  Usage: + inverse\n  Notes: none\n"""

		if len(args) == 0: # using it in interactive mode, inversing user supplied vectors.
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
			VecPrompt.do_input(self,"xyz " + str(inversed_vec[0]) + " " + str(inversed_vec[1])+ " " + str(inversed_vec[2]))
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
