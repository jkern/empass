#!/usr/bin/python
"""empass - Reusable Mnemonic Passwords

Usage: python empass.py [options]

Options:
  -l ..., --length= ...   length of random password (defaults to 8)
  -p ..., --phrase= ...   mnemonic phrase (Should be easily memorizable, but NOT easily guessable)
  -a, --alt               if chosen will alternate hands during password generation
  -h, --help              displays this help

Examples:
  empass.py -p phrase             generates an 8 character password and table based on phrase
  empass.py -p phrase -l 16       generates a 16 character random password and table based on phrase
  empass.py -p phrase -l 16 -a    generates same as above
  empass.py -h                    displays this help

empass is based on the Perdue CERIAS presentation by Umut Topkara, 
"Passwords Decay, Words Endure: Towards Secure and Re-usable Multiple Password Mnemonics"
EMPATHE: rEusable Mnemonics for Password AuTHEntication"""

__author__ = "Joseph Kern (joseph.a.kern@gmail.com)"
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2007/05/21 23:26:06 $"
__copyright__ = "Copyright (c) 2007 Joseph Kern"
__license__ = "BSD"

import sys
import string
import getopt
import random
from random import Random

#Global Variables
#All keys avalible from the right-hand
righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB&*()_+}{|":>?<-=[]\';,./'
#All keys avalible from the left hand
lefthand = '789yuiophjknmYUIPHJKLNM~!@#$%^`'
#The alphabet
alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
alphadict = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','j':'10','k':'11','l':'12','m':'13','n':'14','o':'15','p':'16','q':'17','r':'18','s':'19','t':'20','u':'21','v':'22','w':'23','x':'24','y':'25','z':'26'}

def usage():
    print __doc__

def alphagen():
	alphastr = string.join(alpha)
	return alphastr

def rowgen(phrase): 
	phraselen =len(phrase) - 1
	negphraselen = phraselen * -1
	rowrange = range(negphraselen, phraselen)
	return rowrange

def passwdgen(passwordLength, alternate_hands):
	allchars = righthand + lefthand
	rng = Random()
	randpass = [ ]
	
	for i in range(passwordLength):
		if not alternate_hands:
			randpass.append( rng.choice(allchars) )
		else:
			if i%2:
				#Is used to output a random number
				randpass.append( rng.choice(allchars) )
			else:
				randpass.append( rng.choice(allchars) )
	#Un-comment the following lines to return as a string
	#password = string.join(randpass,'')
	#return password
	#Retrun as a list, this is the best way because the inserting of the password chars into the jumble use the list replace method
	return randpass
	
def phraseslice(phrase):
	phraselen = len(phrase)
	phrasestop = 0
	phraselist = [ ]
	while phrasestop < phraselen:
		#Here is a bit of magic, letters to numbers via the alphadict, and the slicing of the phrase variable by the interation, it is used in the jumblelines function to find the entry in the list to replace with the password variable
		phraselist.append( alphadict[phrase[phrasestop]] )
		phrasestop = phrasestop + 1
	return phraselist
	
def jumblelines(passwordLength, rowrange, phraselist, phrase, password):
	#The following is where you can determin how many rows will be inserted
	#x will equal the ammount of rows and the offset of the rows should default to 4 less than the length
	#turn into a sys arg
	x = 0
	passwordLength = passwordLength - x 
	passloc = 0 + x
	#Loop the print of the jumbles
	while passwordLength > 0:
		row = random.sample(rowrange, 1)
		row = int( row[0] )
		row = row + 1
		phraserow = int(phraselist[row])
		phraserow = phraserow - 1
		jumblerow = passwdgen(25, False)
		if phraserow > 0:
			jumblerow.insert( phraserow, password[passloc] )
		else:
			jumblerow.insert( phraserow * -1, password[passloc] )
		#print password[x]
		if row >= 0:
			row = row + 1
			row = str(row)
		else:
			row = str(row)
		jumblerowstr = string.join(jumblerow)
		print row.zfill(2),"\t",jumblerowstr
		passwordLength = passwordLength - 1
		passloc = passloc + 1

def main(argv):
	passwordLength = 8
	alternate_hands = False
	try:
		opts, args = getopt.getopt(argv, "hjl:p:a", ["help", "justpass","length=", "phrase=", "alt"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-j", "--justpass"):
			password_only = True
		elif opt in ("-l", "--length="):
			passwordLength = int(arg)
		elif opt in ("-p", "--phrase="):
			phrase = arg
		elif opt in ("-a", "--alt"):
			alternate_hands = True
	"""
	if len(args) > 1:
			usage()
			sys.exit()
	"""
	rowrange = rowgen(phrase)
	password = passwdgen(passwordLength, alternate_hands)
	phraselist = phraseslice(phrase)

	print "Phrase:",phrase
	print "Password", string.join(password),"\n\n\n\n"
	print "\t",alphagen()
	jumblelines(passwordLength,rowrange,phraselist,phrase,password)

#Run the program
if __name__ == "__main__":
	main(sys.argv[1:])
