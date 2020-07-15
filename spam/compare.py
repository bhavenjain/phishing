import re
import string
from collections import Counter

def findingUrls(x):
	#finding the links in the message
	fhand = open(x)
	inputString = fhand.read()
	"""
	regex=ur"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
	links = re.findall(regex, inputString)
	"""

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


#message in txt file
fname = "words.txt"
fname_1 = "words.txt"
try:
	fhand = open(fname)
	fhand_1 = open(fname_1)
except:
    print('File cannot be opened:', fname)

#phishing sites
data = "database.txt"
try:
	fdata = open(data,'r+')
except:
    print('File cannot be opened:', data)


#brand name database
Branding = "brand.txt"
try:
	fbrand = open(Branding,'r+')
except:
    print('File cannot be opened:', Branding)


#English words database
fwords = open("word.txt")
#end

wordDatabase = []
work = []
message = []
companyName = []
brand = []
companies = []


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
links = findingUrls(fname)

#making 62lakh urls list:
phishfile = 't.txt'
phishtank = findingUrls(phishfile)

#removing links and making a list of words name MESSAGE
brandCompare = []
for line in fhand_1:
	line = line.rstrip()
	line = line.split()
	brandCompare.append(line)


for word in brandCompare:
	#print(word)
	for i in word:
		if i in links:
			word = word.remove(i)

for word in brandCompare:
	for i in word:
			message.append(i)
#end


#removing special characters froms words and storing it in companyName
#And shorting of the message to gain the company name
for word in message:
	word = word.translate(word.maketrans('','',string.punctuation))#replacingSpecialCharacters(word)
	word = word.lower()
	companyName.append(word)

for i in companyName:
	if i in brand:
		brandName = i

for i in reversed(companyName):
	if i.isdigit() == 1:
		companyName.remove(i)
	if i in wordDatabase:
		companyName.remove(i)
companyName = Remove(companyName)
#end

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

#result
rcheck = 0
print('\n')
for i in links:
	if i in work or i in phishtank:
		print("This is a phishing site..!")
		print('Site:',i)
		print('\n')
		rcheck = 1
	else:
		print("You are safe to use this url:",i)
		print('\n')

if rcheck == 1:
	if len(companies)==1:
		print ('The company its trying to fraud is:',companies[0])
	else:
		print("The companies its trying to Fraud are:")
		i = 0
		while i<len(companies):
			print(companies[i])
			i = i+1
print('\n')
