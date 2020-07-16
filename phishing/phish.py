from collections import Counter
import re
import os
import string
import sys


def clear():
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')


#to find the url in the string
def findingUrls(x):
  inputString = x
  links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', inputString)
  return links


#to find the url in the string
def phishtankUrls():
  try:
  	fphishtank = open('phishtank.txt', 'r+').read()
  except:
  	print("Phishtank.txt was not found")
  links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fphishtank)
  return links



#spell check algorithm
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('brands.txt').read()))

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

# End of spell check






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


# Word Dictionary
try:
	fwords = open('words.txt', 'r+')
	words = []
	for i in fwords:
		i = i.rstrip().lower()
		words.append(i)
except:
	print("Words.txt was not found")


# Brand List
try:
	fbrand = open('brands.txt', 'r+')
	brands = []
	for i in fbrand:
		i = i.rstrip().lower()
		brands.append(i)
except:
	print("Brands.txt was not found")

# Phistank database
phishtank = phishtankUrls()

# Blacklisted sites
try:
	fblack = open('blacklisted.txt', 'r+')
except:
	print("Blacklisted.txt was not found")


# Blacklisted database
try:
	fdatabase = open('database.txt', 'r+')
except:
	print("Database.txt was not found")



# Primary input
mail = '''
Hi Keshav,
	This mail is meant to inform you that you're FACEBOOK password will expire in 24 Hours.
	Please follow the link below to update your password.

http://itoken-suporte30h.ddns.net:2019/token/token-app.tk/loader.php
https://www.facebook.com
'''

# List of the links if any
link = findingUrls(mail)

# list of the mail
mailList = mail.split()
mails = []
for i in mailList:
	i = i.lower()
	mails.append(i)
mailList.clear()

MailBrands = []
names = []
for i in reversed(mails):
	if i in words:
		mails.remove(i)
	elif i in link:
		mails.remove(i)
	elif digitcheck(i) == 1:
		 mails.remove(i)
	else:
		i = i.translate(i.maketrans('','',string.punctuation))
		names.append(i)
		if i in brands:
			MailBrands.append(i)
			continue
		elif i in words:
			names.remove(i)

for i in names:
	if i in MailBrands:
		names.remove(i)

print(names)
print(brands)
