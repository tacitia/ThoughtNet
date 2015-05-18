# take a set of pubmed records downloaded using medline option, and extract all keywords
from collections import Counter
from fuzzywuzzy import fuzz

def extract_all_keywords(filenames):
	results = []
	for filename in filenames:
		input_file = open(filename, 'r')
		keywords = [line.split('- ')[1].strip() for line in input_file if line.startswith('OT  ')]	
		results += list(set(keywords))
	return results


def extract_all_mesh(filenames):
	results = []
	for filename in filenames:
		input_file = open(filename, 'r')
		meshs = [line.split('- ')[1].strip() for line in input_file if line.startswith('MH  ')]	
		results += list(set(meshs))
	return results
	
# returns keyword extracted for the best match to the given title; if no good match, return None
def extract_best_match_keywords(filename, title):
	best_match = {
		score: 0,
		title: None,
		keywords: [],
		flag: False
	}
	input_file = open(filename, 'r')
	for line in input_file:
		if line.startswith('TI'):
			current = line.split('- ')[1].strip()
			score = fuzz.ratio(current, title)
			best_match[score] = score if score > best_match[score] else best_match[score]
			best_match[title] = current if score > best_match[score] else best_match[title]
			best_match[keywords] = [] if score > best_match[score] else best_match[keywords]
			best_match[flag] = True if score > best_match[score] else False
		if line.startswith('OT') and best_match[flag]:
			best_match[keywords].append(line.split('- ')[1].strip())
	if best_match[score] > 85:
		return best_match_keywords
	else:
		return None
	
# return the keywords that have repeated in a certain number of records
def extract_repeated_keywords(filenames, threshold=0):
	keywords = []
	num_record = 0
	for filename in filenames:
		print filename
		input_file = open(filename, 'r')
		for line in input_file:
			if line.startswith('TI'):
				num_record += 1
			if line.startswith('OT'):
				k = line.split('- ')[1].strip()
				if k != 'NOTNLM':
					keywords.append(k)
	keyword_counts = Counter(keywords)
	results = {}
	for key in keyword_counts:
		if keyword_counts[key] > threshold:
			results[key] = keyword_counts[key]
	return results
	
	