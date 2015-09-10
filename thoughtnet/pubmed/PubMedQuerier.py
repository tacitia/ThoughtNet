# -*- coding: utf-8 -*-

# this script is called when
# 1. KnowledgeNet receives initial queries provided by the user
# 2. The association builder is extending the concept graph

import subprocess
import os.path
import PubMedParser
from time import sleep
import operator
import linecache

def query_pubmed(param, savefile, logfile):
	print 'Query: ' + param
	if os.path.isfile(savefile):
		print 'file exists, skip query'
		return
	perl_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'download_pub.pl')
	pipe = subprocess.Popen(['perl', perl_path, param, savefile, '5000', logfile], stdin=subprocess.PIPE)
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
	# issue query for each publication; cannot post more than 3 queries per second!
	titles = input.split('\n')
	filenames = []
	for i, t in enumerate(titles):
		param = convert_title_to_query_param(t)
		f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'queryresults', prefix + '_' + str(i) + '.txt')
		logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'queryresults', prefix + '_' + str(i) + '_log' + '.txt')
		query_pubmed(param, f, logfile)
		filenames.append(f)
		sleep(0.5)	
	return filenames

def extract_terms_for_titles(titles, min_repeat=0):
	# todo: auto increment this
	query_id = '1'
	filenames = download_records(titles, 'query_' + query_id)
#	keywords = PubMedParser.extract_all_keywords(filenames)
	keywords = PubMedParser.extract_repeated_keywords(filenames, min_repeat)
#	keywords = PubMedParser.extract_all_mesh(filenames)
	return keywords

def find_neighbors_for_terms(terms, num_neighbors=10):
	query = ''
	for t in terms:
		query += t + ' '
	f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'queryresults', query + '.txt')
	logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'queryresults', query + '_log' + '.txt')
	query_pubmed(query, f, logfile)
	keywords = PubMedParser.extract_repeated_keywords([f], 0)
	keywords = merge_terms(keywords, terms)
	sorted_keywords = sorted(keywords.items(), key=operator.itemgetter(1), reverse=True)
	num_keywords_all = len(sorted_keywords)
	pub_counts = read_counts(logfile)
	pub_counts['keyword_count'] = num_keywords_all
	pub_counts['showing_count'] = num_neighbors 
	return {'keywords': sorted_keywords[:num_neighbors], 'log': pub_counts}

def search_pubs(query, num_pubs=50):
	f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'queryresults', query + '.txt')
	logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'queryresults', query + '_log' + '.txt')
	query_pubmed(query, f, logfile)
	contents = PubMedParser.read_contents(f, num_pubs)
	pub_counts = read_counts(logfile)
	pub_counts['showing_count'] = num_pubs
	return {'contents': contents, 'log': pub_counts}

def read_counts(logfile):
	orig_count = linecache.getline(logfile, 1)
	count = linecache.getline(logfile, 2)	
	return {'orig_count': orig_count, 'count': count}

def merge_terms(terms, source):
	results = {}
	for key in terms.keys():
		newkey = key.lower()
		toSkip = False
		for r in source:
			if r.lower() == newkey:
				toSkip = True # skip the terms that are the same as the sources
		if toSkip:
			continue
		if newkey in results:
			results[newkey] += terms[key]
		else:
			results[newkey] = terms[key]
	return results

