from fuzzywuzzy import fuzz

file = open('neuroscience.txt')

# target = 'The architecture of cognitive control in the human prefrontal cortex'
target = 'FMRI evidence for a hierarchical organization of the prefrontal cortex'

for line in file:
	if line.startswith('TI'):
		title = line.split('- ')[1].strip()
		similarity = fuzz.ratio(target, title)
		if similarity > 60:
			print target
			print title
			print similarity