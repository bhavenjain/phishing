import re
import os
import sys
import json
import string
import sklearn
import requests
import _pickle as c 
import pyinputplus as py
from collections import Counter

def findingUrls(x):
  inputString = x
  links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', inputString)
  return links
  #end


def findingUrls1(x):
  #finding the links in the message
  fhand = open(x)
  inputString = fhand.read()
  links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', inputString)
  return links
  #end

#spell check algorithm
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('brand.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

#end

#checking the digits
def digitcheck(x):
  check = x.isdigit()
  if check == True:
    return 1
  else:
    return 0

#duplicate REMOVAL
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

#Highest used site for a company

def clear():
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')

def number():
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


# main function

#phishing sites from openphish

data = "database.txt"
fdata = open(data,'r+')

#original sites database
try:
    original = open('websites.txt')
except:
    print('websites.txt not present')

#brand name database
Branding = "brand.txt"
fbrand = open(Branding,'r+')

#English words database
fwords = open("word.txt")
#end

#making 62lakh urls list:
phishfile = 't.txt'
phishtank = findingUrls1(phishfile)

#all the lists

wordDatabase = []
work = []
brand_database = []
message = []
companyName = []
brand = []
companies = []
real = []

#input
mail = """hello you have won a ame.zon chimera investment voucher worth of 500 rupee
please follow the link given below to avail all the benefit"""

#list for brand name
for name in fbrand:
  name = name.rstrip()
  name = name.lower()
  name = name.translate(name.maketrans('','',string.punctuation))
  brand.append(name)

#list for english WORDS
for i in fwords:
  i = i.rstrip()
  i = i.lower()
  i = i.translate(i.maketrans('','',string.punctuation))
  wordDatabase.append(i)

for i in wordDatabase:
  if i in brand:
    wordDatabase.remove(i)

#phishing sites database
for line in fdata:
  line = line.rstrip()
  work.append(line)

#finding urls in the message stored in links
links = findingUrls(mail)

#removing links and making a list of words name MESSAGE
brandCompare = mail.split()

for i in brandCompare:
  if i in links:
    brandCompare.remove(i)



message = brandCompare

twoWord = []
threeWord = []
FourWord = []

for word in message:
  word = word.translate(word.maketrans('','',string.punctuation))
  word = word.lower()

variable = 0

for i in message:
    two = [' '.join(message[variable:variable+2])]
    variable = variable+1
    twoWord.append(two)

variable = 0
for i in message:
    three = [' '.join(message[variable:variable+3])]
    variable = variable+1
    threeWord.append(three)

variable = 0
for i in message:
    four = [' '.join(message[variable:variable+4])]
    variable = variable+1
    FourWord.append(four)



for i in twoWord:
  if i in brand:
    print('1')
    companies.append(i)

for i in threeWord:
  if i in brand:
    companies.append(i)

for i in FourWord:
  if i in brand:
    companies.append(i)


for i in reversed(companyName):
  if i.isdigit() == 1:
    companyName.remove(i)
  if i in wordDatabase:
      companyName.remove(i)

companyName = Remove(companyName)

#original sites check
for url in original:
    url = url.strip()
    real.append(url)

#did you mean on the companyName
for i in companyName:
  correct = correction(i)
  print(correct)
  companies.append(correct)
companies = Remove(companies)

#if its a persons name its not in word directory or a company name
for i in companies:
  if i not in wordDatabase:
    if i not in brand:
      companies.remove(i)





