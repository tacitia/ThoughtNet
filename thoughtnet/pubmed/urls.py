from django.conf.urls import patterns, include, url
from pubmed.views import *

#TODO: modify it so that getDatasets takes in user_id and dataset_id as parameters
urlpatterns = patterns('',
	url(r'^query/title$', process_title_query, name='processTitleQuery'),
	url(r'^query/term$', process_term_query, name='processTermQuery'),
	url(r'^query/pubs$', search_pubs, name='searchPubs'),
)
