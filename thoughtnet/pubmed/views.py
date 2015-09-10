from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import PubMedQuerier as pq


@csrf_exempt
def process_title_query(request):
	if request.method == 'POST':
		 query = request.POST['query']
		 response_data = pq.extract_terms_for_titles(query, min_repeat=1)
	print 'Extracted terms:'
	print response_data
	return HttpResponse(json.dumps(response_data), content_type='application/json')

@csrf_exempt
def process_term_query(request):
	if request.method == 'POST':
		query = request.POST.getlist('query[]')
		response_data = pq.find_neighbors_for_terms(query)		
	print response_data
	return HttpResponse(json.dumps(response_data), content_type='application/json')
	
@csrf_exempt
def search_pubs(request):
	if request.method == 'POST':
		query = request.POST.get('query')
		response_data = pq.search_pubs(query)
	print response_data
	return HttpResponse(json.dumps(response_data), content_type='application/json')	
	