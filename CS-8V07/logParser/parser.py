#!/usr/bin/python3

# Kunal Mukherjee
# Log Paerser
# 10/17/19

#import library
import sys
import time

#Global file name to read the data from
inputFilename = "test.dat"
outputFilename = "server_" + time.strftime("%Y%m%d-%H%M%S") + ".log"
print (outputFilename)
	
# the main driver program
def main():
	# Open the output file
	outputFilehandle = open(outputFilename, "w+")
	outputFilehandle.write("\nNEW REQUEST:\n")

	# Keep reading lines from the input log and process it
	with open(inputFilename, 'r') as inputFilehandle:
		for inputLine in inputFilehandle:
			# print(inputLine)
			outLine = bytes(inputLine, 'utf-8').decode('unicode_escape')
			# print(outLine)
			outputFilehandle.write(outLine)
			# A special expression to mark a new request
			if "edns_client_subnet" in outLine:
				outputFilehandle.write("\nNEW REQUEST:\n")

	outputFilehandle.close()

if __name__ == '__main__':
    main()