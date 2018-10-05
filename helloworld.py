#First python program 

n = "newline\n"
h = "Hello World";
print(n + h + n)
print(str(type(n)) + n)
print(len(h))
print(h[0:len(h)])
print(h[6:len(h)].upper())

""" comment out 
print(n + "Enter something: ")

x = input();

print(n + "You entered: " + x);

templist = ["apple", "banana", "cherry"]

for t in templist:
	print(t)
"""



def temp_function():
	if -1 > 8:
		print("nope")
		print("also nope")
	elif -1 < 8 and 0 > -1:
		print("yep")
	else:
		print("why")
		print("nothing")
	print("printed")

temp_function()


class Temp:
	def __init__(this, temp1, temp2):
		this.temp1 = temp1
		this.temp2 = temp2

	def class_function(this, word = "HelloWorld"):
		this.temp1 = word

t1 = Temp("one", "two")
print(t1.temp1)
print(t1.temp2)
t1.class_function("three")
print(t1.temp1)



