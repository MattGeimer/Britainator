#Britainator is a python program written by Matt Geimer
import fractions

#Defines numInput, a function that will repeat a question until an integer is entered
def numInput(message):
	inp = input(message)
	while True:
		try:
			inp = int(inp)
		except ValueError:
			inp = input(message)
		else:
			return inp
			break

#SETUP
'''
MANUAL OVERRIDE: PICK P Q AND E VALUES AND SET MANOVERRIDE TO 1
WARNING: DO NOT PERFORM THIS ACTION UNLESS YOU KNOW WHAT YOU ARE DOING, IT COULD BREAK THE PROGRAM
'''
manOverride = 0

# p and q are prime numbers that when multiplied together are greater than and coprime to e
p = 0
q = 0
e = 0


def phi(n):
	amount = 0

	for k in range(1, n + 1):
		if fractions.gcd(n, k) == 1:
			amount += 1

	return amount

def gcd(x, y):
   """This function implements the Euclidian algorithm
   to find G.C.D. of two numbers"""
   while(y):
       x, y = y, x % y

   return x

# define lcm function
def lcmFunc(x, y):
   """This function takes two
   integers and returns the L.C.M."""
   lcmTemp = (x*y)//gcd(x,y)
   return lcmTemp

#opens config to check if run before and if config is correctly setup
filein = open("config.txt", 'r')
fdat = filein.readlines()
for i in range(0,len(fdat)):
	fdat[i] = eval(fdat[i])
filein.close()
#First line of config is first run or not (1 is no)
#If fdat (config) is less than necessary 8 parts, add in 0s until there are 8 parts and rerun first setup
if(len(fdat)<=7):
	fdat = []
	while(len(fdat)<8):
		fdat.append(str(0) + '\n')
	fileout = open("config.txt", 'w')
	fileout.writelines(fdat)
	fileout.close()
	filein = open("config.txt", 'r')
	fdat = filein.readlines()
	filein.close()
	r1 = 0
else:
	r1 = fdat[0]

if(r1 == 1):
	#If not first run, read data with long process time and check other data that affects LCM is changed
	lcmt = open("config.txt", 'r')
	fdat = lcmt.readlines()
	for i in range(0,len(fdat)):
		fdat[i] = eval(fdat[i])
	lcmt.close()
	lcm = fdat[1]
	p = fdat[2]
	q = fdat[3]
	n = p * q
	e = fdat[4]
if(r1 == 0):
	if(manOverride == 0):
		p = numInput("Enter a prime number: ")
		q = numInput("Enter a prime number: ")
		n = p * q
		e = numInput("Enter a number less than and coprime to " + str(n) + ": ")
	else:
		n = p * q
	#Find Euler's totient
	lcm = lcmFunc((p-1),(q-1))
	#^ Longest processing time
	#Open config file and load into fdat list
	fileout = open("config.txt", 'r')
	fdat = fileout.readlines()
	fileout.close()
	fileout = open("config.txt", 'w')
	#Change fdat list to record parameters and required data
	fdat[0] = str(1) + '\n'
	fdat[1] = str(lcm) + '\n'
	fdat[2] = str(p) + '\n'
	fdat[3] = str(q) + '\n'
	fdat[4] = str(e) + '\n'
	#Save data to config
	fileout.writelines(fdat)
	fileout.close()
	print("Your RSA encryption system is now set up with the parameters provided")
	if(type(lcm/e) == 'float'):
		#Ensure parameter of RSA is correct
		raise Exception('Your encryption key is not coprime with lcm (try a different number)')


def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)


def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % m
#^ Define Modular Multiplicitive Inverse Finder
#Find modular multiplicitive inverse of encryption key
d = modinv(e, lcm)

if(r1 == 0):
	#If first run, then add chinese remainder theorum numbers to config
	fileout = open("config.txt", 'r')
	fdat = fileout.readlines()
	fileout.close()
	dp = d % (p-1)
	dq = d % (q-1)
	qinv = modinv(q, p)
	fileout = open("config.txt", 'w')
	fdat[5] = str(dp) + '\n'
	fdat[6] = str(dq) + '\n'
	fdat[7] = str(qinv) + '\n'
	fileout.writelines(fdat)
	fileout.close()
else:
	#Otherwise load chinese remainder theorum numbers from config
	filein = open("config.txt", 'r')
	fdat = filein.readlines()
	filein.close()
	dp = eval(fdat[5])
	dq = eval(fdat[6])
	qinv = eval(fdat[7])


def ersa(m, e, n):
	m = ord(m)
	#ENCRYPTION
	m = (m ** e) % n
	return m
#^Encryption algorithm


def drsa(m, d, n):
	#DECRYPTION
	m = (m ** d) % n
	m = chr(m)
	return m
#^Old decryption algorithm (Slow, not used)


def drsaa(m,dp,dq,p,q):
	m1 = (m ** dp) % p
	m2 = (m ** dq) % q
	h = (qinv * (m1 - m2)) % p
	m = m2 + (h * q)
	return chr(m)
#^New decryption algorithm using Chinese Remainder Theorum


while True:
	ed = str(input("Encrypt of Decrypt: ")).upper()
	if(ed == "E" or ed == "ENCRYPT"):
		output = []
		m = input("Enter message: ")
		k = numInput("Enter Public Key: ")
		print("YOUR N is: " + str(n))
		k2 = numInput("Enter N Value: ")
		for letter in m:
			output.append(ersa(letter, k, k2))
		print(output)
	elif(ed == "D" or ed == "DECRYPT"):
		output = ""
		m = eval(input("Enter list: "))
		i = 0
		plast = 0
		for item in m:
			output += drsaa(item,dp,dq,p,q)
			perc = round(i / len(m) * 100, 0)
			if(perc > plast):
				plast = perc
				print(str(perc) + "%")
			i += 1
		print(output)
	elif(ed == "DATAE"):
		data = []
		datain = open("data.txt", 'r')
		data = datain.readlines()
		datain.close()
		output = []
		k = numInput("Enter Public Key: ")
		print("YOUR N is:", end=" ")
		print(n)
		k2 = numInput("Enter N Value: ")
		i=0
		for item in data:
			m = data[i]
			output = []
			for letter in m:
				output.append(ersa(letter, k, k2))
			data[i] = str(output) + '\n'
			i += 1
		dataout = open("data.txt", 'w')
		dataout.writelines(data)
		dataout.close()
		data = []
	elif(ed == "DATAD"):
		datain = open("data.txt", 'r')
		data = datain.readlines()
		datain.close()
		i=0
		for item in data:
			output = ""
			m = eval(data[i])
			plast = 0
			output = ""
			for char in m:
				#Debug drsaa function inputs --> print("Char: "+str(char)+" DP: "+str(dp)+" DQ: "+str(dq)+" P: "+str(p)+" Q: "+str(q))
				output += drsaa(char, dp,dq,p,q)
			data[i] = output
			i += 1
		dataout = open("data.txt", 'w')
		dataout.writelines(data)
		dataout.close()
		print("Decryption Completed")
	elif(ed == "Q" or ed == "QUIT"):
		print("Quitting Program")
		break
	else:
		print("Please enter 'e' or 'd'")
