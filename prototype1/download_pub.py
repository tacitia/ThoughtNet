# -*- coding: utf-8 -*-

# this script is called when
# 1. KnowledgeNet receives initial queries provided by the user
# 2. The association builder is extending the concept graph

import subprocess
import os.path
import PubMedParser
from time import sleep

def query_pubmed(param, savefile):
	print 'Query: ' + param
	if os.path.isfile(savefile):
		print 'file exists, skip query'
		return
	pipe = subprocess.Popen(['perl', './download_pub.pl', param, savefile], stdin=subprocess.PIPE)
	pipe.wait()
	
# seems like Esearch does search differently from the pubmed search bar. Sometimes a title query yields 
# no results while pubmed search can return an exact match...assigning low priority to this issue
# Example: Rostral–caudal gradients of abstraction revealed by multivariate pattern analysis of working memory
def convert_title_to_query_param(input):
	result = input
	result = result.replace(' ', '+')
	return result
	
def convert_concept_to_query_param(input):
	result = input
	result = result.replace('"', '%22') # need to double check if this is necessary
	return result

def download_records(input, prefix):
	titles = input.split('\n')
	filenames = []
	for i, t in enumerate(titles):
		param = convert_title_to_query_param(t)
		f = prefix + '_' + str(i) + '.txt'
		query_pubmed(param, f)
		filenames.append(f)
		sleep(0.5)	
	return filenames

# the input should be either a list of titles or a list of terms, separated by \n
input = 'The architecture of cognitive control in the human prefrontal cortex\nFMRI evidence for a hierarchical organization of the prefrontal cortex\nRostral–caudal gradients of abstraction revealed by multivariate pattern analysis of working memory'
input_option = 'title' # either "term" or "title"
query_id = '1'
assoc_option = 'group' # either "group" or "individual"

# Step 1: generate 0-level keywords that are directly from user inputs
if input_option == 'title':
	# issue query for each publication; cannot post more than 3 queries per second!
	filenames = download_records(input, 'query_' + query_id)
#	keywords = PubMedParser.extract_all_keywords(filenames)
	keywords = PubMedParser.extract_repeated_keywords(filenames, 1)
#	keywords = PubMedParser.extract_all_mesh(filenames)
elif input_option == 'term':
	print 'not implemented'
	
# Step 2: generate 1-level keywords
# can do this in two ways: 1) take multiple terms as the same query (group) 2) take each term as a query
if assoc_option == 'group':
	query = ''
	for key in keywords:
		query += key + ' '
	f = query + '.txt'
	query_pubmed(query, f)
	keywords = PubMedParser.extract_repeated_keywords([f], 30)
	print keywords
elif assoc_option == 'individual':
	for key in keywords:
		query_pubmed(key, key + '.txt')	

