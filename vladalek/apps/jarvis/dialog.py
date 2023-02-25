import re
from fuzzywuzzy import process
from .read import get_text
from random import choice

def clean_str(r):
	r = r.lower()
	r = [c for c in r if c in alphabet]
	return ''.join(r)

alphabet = " 1234567890-йцукенгшщзфівапролдячсмитьбюёхїжєqwertyuiopasdfghjklzxcvbnm?%.,()'!:;@"

X_text = []
y = []

def update():
	content = get_text()
	
	blocks = content.split('\n')
	dataset = []
	
	for block in blocks:
		replicas = block.split('\\')[:2]
		if len(replicas) == 2:
			pair = [clean_str(replicas[0]), clean_str(replicas[1])]
			if pair[0] and pair[1]:
				dataset.append(pair)
	
	global X_text
	global y
	
	for question, answer in dataset[:10000]:
		X_text.append(question)
		y += [answer]

update()	

def get_generative_replica(text):
	global X_text
	global y
	question = process.extractOne(text, X_text)[0]
	answer = y[X_text.index(question)]
	answer = answer.split('@')
	return choice(answer)
