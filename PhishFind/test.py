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
    dire = "/Users/Bhaven/bhaven/python/hackathon/buttonpython/emails/"
    files = os.listdir(dire)

    emails = [dire + email for email in files]
    word_email = []
    c = len(emails)

    for email in emails:
        #f = open(email)
        with open(email, 'rb') as f:
            e_var = f.read().decode(errors='replace')
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
    clf = load ("/Users/Bhaven/bhaven/python/hackathon/buttonpython/thefinal.mdl")
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
message = []
companyName = []
brand = []
companies = []
real = []

#input
mail =  sys.argv[1]

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

for word in message:
  word = word.translate(word.maketrans('','',string.punctuation))
  word = word.lower()
  companyName.append(word)

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
  companies.append(correct)
companies = Remove(companies)

#if its a persons name its not in word directory or a company name
for i in companies:
  if i not in wordDatabase:
    if i not in brand:
      companies.remove(i)

if spam_checkAi(mail) == '0':
    aiCheck = 1
else:
    aiCheck = 0

#result
rcheck = 0
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

  # apivoid threat level detection api
  host = data['domain']
  response1 = requests.get(
      "https://endpoint.apivoid.com/threatlog/v1/pay-as-you-go/?key=22e61728908b1f484874fa0245267890958b76be&host=" + host)

  data1 = response1.json()
  try:
    data1 = data1['data']
    data1 = data1['threatlog']
    data1 = data1['detected']
  except:
      pass
  #endd......

  #mutiple api status linkin through apivoid
  host = data['domain']
  response2 = requests.get(
      "https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key=22e61728908b1f484874fa0245267890958b76be&host=" + host + "&exclude_engines=ThreatLog,SpamhausDBL,Spam404")
  data2 = response2.json()
  data2 = data2['data']
  data2 = data2['report']
  data2 = data2['blacklists']
  data2 = data2['engines']

    #different api check
  antisocial = data2['3']
  antisocial = antisocial['detected']

  Badbitcoin = data2['4']
  Badbitcoin = Badbitcoin['detected']

  Bambenek = data2['5']
  Bambenek = Bambenek['detected']

  CERTGIB = data2['7']
  CERTGIB = CERTGIB['detected']

  CERTPA = data2['8']
  CERTPA = CERTPA['detected']

  CRDF = data2['10']
  CRDF = CRDF['detected']

  C_APT_ure = data2['6']
  C_APT_ure = C_APT_ure['detected']

  CoinBlocker = data2['9']
  CoinBlocker = CoinBlocker['detected']

  CyberCrime = data2['11']
  CyberCrime = CyberCrime['detected']

  DShield = data2['12']
  DShield = DShield['detected']

  EtherAddressLookup = data2['13']
  EtherAddressLookup = EtherAddressLookup['detected']

  EtherScamDB = data2['14']
  EtherScamDB = EtherScamDB['detected']

  Fumik0 = data2['15']
  Fumik0 = Fumik0['detected']

  HijackedUrls = data2['16']
  HijackedUrls = HijackedUrls['detected']

  Joewein = data2['17']
  Joewein = Joewein['detected']

  Malc0de = data2['18']
  Malc0de = Malc0de['detected']

  MalwareDomainList = data2['19']
  MalwareDomainList = MalwareDomainList['detected']

  MalwarePatrol = data2['20']
  MalwarePatrol = MalwarePatrol['detected']

  MetaMask = data2['21']
  MetaMask = MetaMask['detected']

  NABP = data2['22']
  NABP = NABP['detected']

  Netlab360 = data2['23']
  Netlab360 = Netlab360['detected']

  OpenPhish = data2['24']
  OpenPhish = OpenPhish['detected']

  PhishingDatabase = data2['25']
  PhishingDatabase = PhishingDatabase['detected']

  PhishFeed = data2['26']
  PhishFeed = PhishFeed['detected']

  PhishStats = data2['27']
  PhishStats = PhishStats['detected']

  PhishTank1 = data2['28']
  PhishTank1 = PhishTank1['detected']

  Quttera = data2['30']
  Quttera = Quttera['detected']

  Ransomware = data2['31']
  Ransomware = Ransomware['detected']

  RPiList = data2['32']
  RPiList = RPiList['detected']

  SquidBlacklist = data2['33']
  SquidBlacklist = SquidBlacklist['detected']

  Threat = data2['35']
  Threat = Threat['detected']

  ThreatCrowd = data2['35']
  ThreatCrowd = ThreatCrowd['detected']

    #phishtank api
  if i in phishtank:
    print("This is a phishing site : " , i)
    print('The main domain:', data['domain'])
    try:
      reg = regiContacts[0]
      print("Organization name: ",reg['organization'])
    except:
      pass
    rcheck = 1

  elif i in work:
    print("This is a phishing site : " , i)
    print('The main domain:', data['domain'])
    try:
      reg = regiContacts[0]
      print("Organization name: ",reg['organization'])
    except:
      pass
    rcheck = 1

# non registered sites
  elif data['registered?'] == False:
     print("This seems to be a phishing site as its not a registered one")
     print('Site:', i)
     print('The main domain:', data['domain'])
     try:
         reg = regiContacts[0]
         print("Organization name: ", reg['organization'])
     except:
         pass
     rcheck = 1


    #different api check apivoid check and diff api results
  elif antisocial == True:

      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif Badbitcoin == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif Bambenek == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif CERTPA == True:

      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif CERTGIB == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif C_APT_ure == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
         reg = regiContacts[0]
         print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif CoinBlocker == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif CyberCrime == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif CRDF == True:
     print("This is a blacklisted site : ", i)
     print('The main domain:', data['domain'])
     try:
         reg = regiContacts[0]
         print("Organization name: ", reg['organization'])
     except:
         pass
     rcheck = 1

  elif DShield == True:
     print("This is a blacklisted site : ", i)
     print('The main domain:', data['domain'])
     try:
         reg = regiContacts[0]
         print("Organization name: ", reg['organization'])
     except:
         pass
     rcheck = 1

  elif EtherAddressLookup == True:
     print("This is a blacklisted site : ", i)
     print('The main domain:', data['domain'])
     try:
         reg = regiContacts[0]
         print("Organization name: ", reg['organization'])
     except:
         pass
     rcheck = 1

  elif EtherScamDB == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:

          pass
      rcheck = 1

  elif Fumik0 == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:

          pass
      rcheck = 1

  elif HijackedUrls == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:

          pass
      rcheck = 1

  elif Joewein == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:

          pass
      rcheck = 1


  elif Malc0de == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1


  elif MalwareDomainList == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif MalwarePatrol == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif MetaMask == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif NABP == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1


  elif Netlab360 == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif OpenPhish == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif PhishingDatabase == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif PhishFeed == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif PhishStats == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif PhishTank1 == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif Quttera == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif Ransomware == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif RPiList == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif SquidBlacklist == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif Threat == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:

          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  elif ThreatCrowd == True:
      print("This is a blacklisted site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  #apivoid api check reputation check
  elif data1 == True:
      print("This is a phishing site : ", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass
      rcheck = 1

  #original sites database check result
  elif data['domain'] in real:
      print("You are safe to use this url:", i)
      print('The main domain:', data['domain'])
      try:
          reg = regiContacts[0]
          print("Organization name: ", reg['organization'])
      except:
          pass

  else:
    if len(links) > 0 and rcheck == 0:
        if aiCheck == 1:
            print("Spam message as detected by our A.I...", end="")
        else:
            print("This appears to be a safe message", end="")
            print('The main domain:', data['domain'])
            try:
                reg = regiContacts[0]
                print("Organization name: ", reg['organization'])
            except:
                pass

if len(links) == 0:
    print('This does not contain any URL....')

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

else:
    if aiCheck == 1:
        print("Spam message as detected by our A.I...", end="")
    else:
        print("This appears to be a safe message", end="")


#for database creation .....................................................................

if EndResult == 1:
  if len(companies) == 1:
      for i in companies:
          name = companies[0] + '.txt'
          BrandStore = open("/Users/bhaven/bhaven/python/hackathon/brand/" + name,'a+')
          for link in brand_database:
              BrandStore.write(link)
          BrandStore.close()

  elif len(companies) == 0:
    pass

  else:
    i = 0
    for i in companies:
      name = i+'.txt'
      BrandStore = open("/Users/bhaven/bhaven/python/hackathon/brand/" + name,'a+')
      for link in brand_database:
          BrandStore.write(link + "         ")
      BrandStore.close()

# End .......................................................................................
