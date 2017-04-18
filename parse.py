import os
import sys
import operator
import csv

class characters:
	freq = 0
	char = ""     
	def __init__(self, freq, char):
		self.freq = freq
		self.char = char

f = open('cedict_ts.u8', 'r', encoding='utf-8')
dict = {}
for line in f:		
	if line.startswith(("#", "#!")):
		continue
	else:
		trad, simp, definition = line.split(' ', 2)
		dict.update({simp: definition})

		
article = open('article.txt', 'r', encoding='utf-8')
char_freq = {}
c = ""
quit = False
while quit == False or c:
	while len(c) < 4:
		d =  article.read(1)
		if not d:
			quit = True
			break;
		elif (d == '，' or d == '。' or d == ' '):
			continue
		else:
			c += d
	# try 4 character lookup
	try:
		definition = dict[c]			
		try:
			freq = char_freq[c]
			char_freq.update({c: freq + 1})
		except KeyError:
			char_freq.update({c: 1})
		c = ""
	except KeyError:
		#try 3 character lookup
		try:
			definition = dict[c[:3]]
			try:
				freq = char_freq[c[:3]]
				char_freq.update({c[:3]: freq + 1})
			except KeyError:
				char_freq.update({c[:3]: 1})
			c = c[3:]
		except KeyError:
			#try 2 character lookup
			try:
				definition = dict[c[:2]]
				try:
					freq = char_freq[c[:2]]
					char_freq.update({c[:2]: freq + 1})
				except KeyError:
					char_freq.update({c[:2]: 1})
				c = c[2:]
			except KeyError:
				#try 1 character lookup
				try:
					definition = dict[c[0]]
					try:
						freq = char_freq[c[0]]
						char_freq.update({c[0]: freq + 1})
					except KeyError:
						char_freq.update({c[0]: 1})				
					c = c[1:]
				except KeyError:				
					c = c[1:]
					
			

switch = {}
chars = []
for x in char_freq:
	tmp = characters(char_freq[x], x)
	chars.append(tmp)

chars.sort(key=operator.attrgetter('freq'), reverse=True)

	
with open('stats.csv', 'w', newline='') as csvfile:
	stats_csv = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
	stats_csv.writerow(["Stats"])
	stats_csv.writerow(["Word", "Appearances", "Pronunciation", "Meaning"])
	for x in chars:	
		pronunciation_no_newline, junk = dict[x.char].split('\n', 1)
		pronunciation_no_newline = pronunciation_no_newline.replace('|',' ')
		pronunciation_no_newline = pronunciation_no_newline.replace(',',' ')
		pronunciation_no_newline = pronunciation_no_newline.replace('[','')	
		pronunciation_no_newline, definition = pronunciation_no_newline.split(']', 1)
		try:
			stats_csv.writerow([x.char, x.freq, pronunciation_no_newline, definition])
		except UnicodeEncodeError:
			continue;
f.close()

	