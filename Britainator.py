import fractions
#SETUP

#MANUAL
#Choose 2 prime numbers
p = 149
q = 679
#Pick Encryption key (Prime number)
e = 787

#AUTOMATIC (DO NOT TOUCH)
#Euler's Totient of n
n = p * q


def phi(n):
        amount = 0

        for k in range(1, n + 1):
                if fractions.gcd(n, k) == 1:
                        amount += 1

        return amount

filein = open("config.txt", 'r')
fdat = filein.readlines()
r1 = eval(fdat[0])
filein.close()
if(r1 == 1):
        lcmt = open("config.txt", 'r')
        fdat = lcmt.readlines()
        lcmt.close()
        lcm = eval(fdat[1])
        if(p != eval(fdat[2]) or q != eval(fdat[3]) or e != eval(fdat[4])):
                r1 = 0
if(r1 == 0):
        lcm = phi(n)
        fileout = open("config.txt", 'r')
        fdat = fileout.readlines()
        fileout.close()
        fileout = open("config.txt", 'w')
        fdat[0] = str(1) + '\n'
        fdat[1] = str(lcm) + '\n'
        fdat[2] = str(p) + '\n'
        fdat[3] = str(q) + '\n'
        fdat[4] = str(e) + '\n'
        fileout.writelines(fdat)
        fileout.close()

if(type(lcm/e) == 'float'):
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
d = modinv(e, lcm)


def ersa(m, e, n):
        m = ord(m)
        #ENCRYPTION
        m = (m ** e)%n
        return m


def drsa(m, d, n):
        #ENCRYPTION
        m = (m ** d) % n
        m = chr(m)
        return m

while True:
        ed = input("Encrypt of Decrypt: ").upper()
        if(ed == "E" or ed == "ENCRYPT"):
                output = []
                m = input("Enter message: ")
                k = eval(input("Enter Public Key: "))
                print("YOUR N is:", end=" ")
                print(n)
                k2 = eval(input("Enter N Value: "))
                for letter in m:
                        output.append(ersa(letter, k, k2))
                print(output)
        elif(ed == "D" or ed == "DECRYPT"):
                output = ""
                m = eval(input("Enter list: "))
                i = 0
                plast = 0
                for item in m:
                        output += drsa(item, d, n)
                        perc = round(i / len(m) * 100, 0)
                        if(perc > plast):
                                plast = perc
                                print(perc, end="")
                                print("%")
                        i += 1
                print(output)
        elif(ed == "DATAE"):
            data = []
            datain = open("data.txt", 'r')
            data = datain.readlines()
            datain.close()
            output = []
            k = eval(input("Enter Public Key: "))
            print("YOUR N is:", end=" ")
            print(n)
            k2 = eval(input("Enter N Value: "))
            i=0
            for item in data:
                m = data[i]
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
                for item in m:
                    output += drsa(item, d, n)
                    perc = round(i * q / (len(m) * len(data)) * 100, 0)
                    if(perc > plast):
                            plast = perc
                            print(perc, end="")
                            print("%")
                    q += 1
                data[i] = output + '\n'
                i += 1
            dataout = open("data.txt", 'w')
            dataout.writelines(data)
            dataout.close()
            print("Decryption Completed")
        else:
                print("Please enter 'e' or 'd'")
