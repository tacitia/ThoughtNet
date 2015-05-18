# take a set of pubmed records downloaded using medline option, and extract all keywords


input_file = open('neuroscience.txt', 'r')

# step 1: extract all keywords
keywords = []

for line in input_file:
	if line.startswith('OT'):
		keyword = line.split('- ')[1].strip()
		if keyword not in keywords:
			keywords.append(keyword)

print len(keywords)

# step 2: compute co-occurrence

# final step: write keywords and occurrence matrix out to files