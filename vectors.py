#! /usr/bin/env python

####################################
# Python Vector Manipulation Shell #
#      Lyell Read | 6/15/2018      #
####################################

from cmd import Cmd

class VecPrompt (Cmd):

	def do_hello(self,args):
		"""Says Hello. You give it a name it will greet /you/"""
		if len(args) == 0:
			name = ""
		else:
			name = args
			print(args)
		print("Hello, %s" %name)

	def do_calculation(self,args):
		arglist=args.split()
		print (arglist)

	def do_quit(self, args):
		"""Quits the program... Duh"""
		print ("Quitting")
		raise SystemExit


if __name__ == "__main__":
	prompt = VecPrompt()
	prompt.prompt = 'V&> '
	prompt.cmdloop('Starting prompt...')

