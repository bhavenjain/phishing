import re
import os
import sys
import json
import string
import sklearn
import requests
import _pickle as c
from collections import Counter


#the ai code for spam check.......
def load(clf_file):
    with open(clf_file) as par:
        clf = c.load(par)
    return clf
def diction():
    dire = "C:/Users/AGARWALS/Django/emails/"
    files = os.listdir(dire)

    emails = [dire + email for email in files]
    word_email = []
    c = len(emails)
    

    for email in emails:
        f = open(email)
        e_var = f.read()
        word_email += e_var.split(" ") 
        c -= 1
    for i in range(len(word_email)):
        if not word_email[i].isalpha():
            word_email[i] = ""
           
    dictionary = Counter(word_email)
    del dictionary[""]
    return (dictionary.most_common(1500))
def load(clf_file):
    with open(clf_file, 'rb') as par:
        clf = c.load(par)
    return clf


def spam_checkAi(x):
    #result from the ai check 
    clf = load ("C:/Users/AGARWALS/Django/classify.mdl")
    d = diction ()
    features = []
    inp_var = x
    inp_var.split()
    for word in d:
        features.append(inp_var.count(word[0]))
    res = clf.predict([features])
    return (["0", "1"][res[0]])
    #0 not spam, 1 spam

    #enddd .......
    
    
#end for the functions



def findingUrls(x):
  #finding the links in the message
  #fhand = open(x)
  inputString = x#fhand.read()
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

#function to remove special charaters from message words
def replacingSpecialCharacters(x):
  strs = x
  nstr = re.sub(r'[?|$|.|!|,|:|;|*|"|'']',r'',strs)
  nestr = re.sub(r'[^a-zA-Z0-9 ]',r'',nstr)
  return nestr

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


# main function

#phishing sites
data = "database.txt"
fdata = open(data,'r+')

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
message = []
companyName = []
brand = []
companies = []

#input
mail = sys.argv[1]


#list for brand name
for name in fbrand:
  name = name.rstrip()
  name = name.lower()
  name = name.translate(name.maketrans('','',string.punctuation))#replacingSpecialCharacters(name)
  brand.append(name)


#list for english WORDS
for i in fwords:
  i = i.rstrip()
  i = i.lower()
  i = i.translate(i.maketrans('','',string.punctuation))#replacingSpecialCharacters(i)
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

for word in message:
  word = word.translate(word.maketrans('','',string.punctuation))#replacingSpecialCharacters(word)
  word = word.lower()
  companyName.append(word)

for i in reversed(companyName):
  if i.isdigit() == 1:
    companyName.remove(i)
  if i in wordDatabase:
    companyName.remove(i)
companyName = Remove(companyName)

#did you mean on the companyName
for i in companyName:
  correct = correction(i)
  companies.append(correct)
companies = Remove(companies)

#if its a persons name its not in word directory or a company name
for i in companies:
  if i not in wordDatabase:
    if i not in brand:
      companies.remove(i)

            
#if spam_checkAi(mail) == '0':
#    aiCheck = 1
#else:
#    aiCheck = 0
            
#result
rcheck = 0
print('\n')
for i in links:

  # WHOIS API.......
  response = requests.get("https://jsonwhois.com/api/v1/whois",
              headers={
                "Accept": "application/json",
                "Authorization": "Token token=1d1279b6c95fa95219c040f4f3b6a936"
              },
              params={
                "domain": i
              })

  data = response.json()
  try:
    regis = data["registrar"]
  except:
    pass
  try:
    regiContacts = data["registrant_contacts"]
  except:
    pass
  if data['registered?'] == False:
    print("This seems to be a phishing site..!")
    print('Site:', i)
    print('The main domain:',data['domain'])
    try:
      reg = regiContacts[0]
      print("Organization name: ",reg['organization'])
    except:
      print('')
    rcheck = 1



  elif i in phishtank:
    print("This is a phishing site..!")
    print('The main domain:', data['domain'])
    print('Site:',i)
    try:
      reg = regiContacts[0]
      print("Organization name: ",reg['organization'])
    except:
      print('')
    print('\n')
    rcheck = 1

  else:
    print("You are safe to use this url:",i)
    print('The main domain:', data['domain'])
    try:
      reg = regiContacts[0]
      print("Organization name: ",reg['organization'])
    except:
      print('')
    print('\n')

if rcheck == 1:
  if len(companies)==1:
    print ('The company its trying to fraud is:',companies[0].capitalize())
  elif len(companies) == 0:
    pass 
  else:
    print("The companies its trying to Fraud are:")
    i = 0
    while i<len(companies):
      print(companies[i].capitalize())
      i = i+1

"""
else:
    if aiCheck == 1:
        print("Based on our AI this is a spam message.... ")
    else:
        print("Based on our Ai this appears to be a safe message")
"""         
print('\n')