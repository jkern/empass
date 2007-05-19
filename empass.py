#!/usr/bin/python
import sys
import string
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
	print "USAGE:"
	print sys.argv[0],"\n", "[length of password-default to 8]\n",
	print "[phrase key (a word that is 4 letters shorter than the password length)]\n",
	print "[alt (if you want the password to alternate hands)]\n"
def sanityCheck():
	rowrange = rowgen(phrase)
	columnhead = alphagen()
	password = passwdgen(passwordLength, alternate_hands)
	phraselist = phraseslice(phrase)
	passwordstr = string.join(password)
	
	print "Phrase:",phrase
	print "Password",passwordstr,"\n\n\n\n"
	#print "Rowrange:",rowrange
	print "\t",columnhead
	#print "Phraselist:",phraselist,"\n"
	jumblelines(passwordLength, rowrange, phraselist,phrase,password)
def alphagen():
	alphastr = string.join(alpha)
	return alphastr

def rowgen(phrase): 
	phraselen =len(phrase) - 1
	negphraselen = phraselen * -1
	rowrange = range(negphraselen, phraselen)
	#rowrange.remove(0)
	return rowrange

#def format(rowrange, columnhead, random):
	#row = random.sample(rowrange, 1)
	
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
	#x will equal the ammount of rows and the offset of the rows
	#turn into a sys arg
	x = 0
	passwordLength = passwordLength - x 
	#phraselen = len(phrase)
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
			#jumblerow.remove
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
	
try:	
	passwordLength = int(sys.argv[1])
except:
	#user didn't specify a length.  that's ok, just use 8
	passwordLength = 8
try:
	phrase = str(sys.argv[2])
except:
	usage()
try:
	alternate_hands = sys.argv[3] == 'alt'
	if not alternate_hands:
		usage()
except:
	alternate_hands = False

#runit!!!
sanityCheck()
