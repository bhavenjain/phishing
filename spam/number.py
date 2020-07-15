import pyinputplus as pyinp

name = input("Enter the company name:")
file = name + '.txt'

url = []

try:
    fopen = open("/Users/bhaven/bhaven/python/hackathon/brand/" + file)
    for i in fopen:
        i = i.rstrip()
        url = i.split()

except:
    print("The company does not exist in our database.....")

histogram = dict()

for c in url:
    histogram[c] = histogram.get(c,0) + 1

for i in histogram:
    print(i, " --> ",histogram[i])
