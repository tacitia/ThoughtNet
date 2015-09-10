// This file contains settings for AmplifyJS

amplify.request.define('getLeaves', 'ajax', {
	url: '/connectivity/connections/leaves/{connId}/',
	type: 'GET'
})

amplify.request.define('getLocalConnections', 'ajax', {
	url: '/connectivity/connections/local/{structId}/{depth}/',
	type: 'GET'
})

amplify.request.define('getPaths', 'ajax', {
	url: '/connectivity/connections/paths/{sourceId}/{targetId}/{maxHop}/',
	type: 'GET'
})

amplify.request.define('getStructImgMap', 'ajax', {
	url: '/anatomy/structImgMap/',
//	url: 'http://brainconnect.cs.brown.edu/anatomy/structImgMap',
	type: 'GET'
})

amplify.request.define('getConnectionNotes', 'ajax', {
	url: '/account/notes/connection/{userId}/{datasetId}/',
	type: 'GET'
})

amplify.request.define('submitTitleQuery', 'ajax', {
	url: '/pubmed/query/title',
	type: 'POST'
})

amplify.request.define('submitTermQuery', 'ajax', {
	url: '/pubmed/query/term',
	type: 'POST'
})

amplify.request.define('searchPubs', 'ajax', {
	url: '/pubmed/query/pubs',
	type: 'POST'
})


/* Subscriptions */

amplify.subscribe('datasetReady', function(data, datasetId) {
	console.log("Dataset " + datasetId + " received.");
	ui.regionSelector.render(data.nodes);
	ui.attrSelector.render(data.links);
	ui.pathSearch.render(data.nodes);
//	ui.loadingModal.hide();
	svg.renderViews(data, datasetId);
})

amplify.subscribe('renderComplete', function() {
	svg.renderComplete();
})

amplify.subscribe('resetComplete', function() {
	ui.canvasReset.resetComplete();
	ui.pathSearch.resetComplete();
})

amplify.subscribe('userValidationComplete', function() {
	window.userValidated();
})