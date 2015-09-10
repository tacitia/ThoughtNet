var level0Terms = [];
var level1Terms = [];
var pubResults = '';
var titleInputs = null;
var buttons = {};

$(document).ready(function () {
	titleInput = $('#title-input');
	buttons.submitTitles = $('#title-input-submit');
	buttons.getAssocTerms = $('#get-associated-terms');
	buttons.searchPubs = $('#search-pubs');
	
	buttons.submitTitles.click(submitTitles);
	buttons.getAssocTerms.click(getAssocTerms);
	buttons.searchPubs.click(searchPubs);
	
	d3.selectAll('button.close')
		.on('click', function(d) {
			d3.select(this.parentNode)
				.style('display', 'none');
		});
});

var submitTitles = function () {
	var input = titleInput.val();	
	level0Terms.length = 0;
	updateTermDisplay(level0Terms);
	$(this).button('loading');
	amplify.request( 'submitTitleQuery',
		{
			query: input
		},
		function (data) {
			console.log(data);
			for (var key in data) {
				level0Terms.push({
					term: key, 
					repeat: data[key],
					selected: false,
				});
			}
			updateTermDisplay(level0Terms);
			buttons.submitTitles.button('reset');
		}
	);
};

var getAssocTerms = function () {
	var selectedTerms = [];
	for (var i in level0Terms) {
		if (level0Terms[i].selected) selectedTerms.push(level0Terms[i].term);
	}
	for (var i in level1Terms) {
		if (level1Terms[i].selected)  {
			selectedTerms.push(level1Terms[i].term);
			level0Terms.push(level1Terms[i]);
		}
	}
	// also update the visual list of level 0 terms and clear all level 1 terms
	updateTermDisplay(level0Terms);
	level1Terms.length = 0;	
	updateAssocTermDisplay(level1Terms);
	var status = 'Querying PubMed for terms associated with: '
	for (var i in selectedTerms) {
		status += selectedTerms[i];
		if (i != selectedTerms.length-1) { status += ', ' }
	}
	updateAlert('#submit-term-query-alert', status , true);
	updateAlert('#term-downloaded-alert', '' , false);
	$(this).button('loading');
	amplify.request( 'submitTermQuery',
		{
			query: selectedTerms
		},
		function (data) {
			console.log(data); //
			var keywords = data.keywords;
 			for (var i in keywords) {
				level1Terms.push({
					term: keywords[i][0], 
					repeat: keywords[i][1],
					selected: false,
				});
			}
			updateAssocTermDisplay(level1Terms);
			buttons.getAssocTerms.button('reset');
			var summary = 'PubMed returned ' + data.log.orig_count + ' publications given selected keywords. Downloaded the top ' + data.log.count + ' for analysis. Extracted ' + data.log.keyword_count + ' terms in total. Showing the top ' + data.log.showing_count + ' frequent keywords.';
			updateAlert('#term-downloaded-alert', summary, true);
		}
	);	
};

var updateAlert = function(divName, text, show) {
	var alertDiv = d3.select(divName)
	alertDiv.selectAll('p').remove();
	if (show) {
		d3.select(divName).style('display', 'block');
		alertDiv.selectAll('p')
			.data([text])
			.enter()
			.append('p')
			.text(function(d) {
				return d;
			});
	}
	else {
		d3.select(divName).style('display', 'none');
	}
};

// When searching pubs, take all selected level 0 and level 1 terms and issue a query
var searchPubs = function() {
	var query = '';
	for (var i in level0Terms) {
		if (!level0Terms[i].selected) continue
		query += level0Terms[i].term;
		query += ' ';
	}
	for (var i in level1Terms) {
		if (!level1Terms[i].selected) continue
		query += level1Terms[i].term;
		query += ' ';
	}
	updateAlert('#submit-pub-query-alert', 'Querying PubMed with: ' + query, true);
	updateAlert('#pub-downloaded-alert', '' , false);
	$(this).button('loading');
	amplify.request( 'searchPubs',
		{
			query: query
		},
		function (data) {
			pubResults = data.contents;
			populatePubDisplay(pubResults);
			console.log(data);
			var pubResultSummary = 'PubMed returned ' + data.log.orig_count + ' records. Showing the first ' + data.log.showing_count + ' records.';
			updateAlert('#pub-downloaded-alert', pubResultSummary , true);
			buttons.searchPubs.button('reset');
		}
	);	
};

var populatePubDisplay = function (pubResults) {
	var pubDisplay = $('#pub-result-display');
	pubDisplay.val(pubResults);
};

var updateAssocTermDisplay = function (terms) {
	var termDiv = d3.select('#level-1-term-div').select('#term-display-div');
	var buttons = termDiv.selectAll('button')
		.data(terms, function(d) { return d.term+d.repeat; });
	buttons.exit().remove();
	buttons.enter()
		.append('button')
		.attr('class', 'btn btn-default btn-xs')
		.text(function(d) {
			return d.term + ' (' + d.repeat + ')';
		})
		.on('click', function(d) {
			// update the selection
			d3.event.preventDefault();
			d.selected = !d.selected;
			d3.select(this).classed('btn-info', d.selected);
			d3.select(this).classed('btn-default', !d.selected);
		});
};

var updateTermDisplay = function (terms) {
	var termDiv = d3.select('#level-0-term-div').select('#term-display-div');
	var buttons = termDiv.selectAll('button')
		.data(terms, function(d) { return d.term+d.repeat; });
	buttons.exit().remove();	
	buttons.enter()
		.append('button')
		.attr('class', 'btn btn-default btn-xs')
		.classed('btn-info', function(d) {
			return d.selected;
		})
		.text(function(d) {
			return d.term + ' (' + d.repeat + ')';
		})
		.on('click', function(d) {
			// update the selection
			d3.event.preventDefault();
			d.selected = !d.selected;
			d3.select(this).classed('btn-info', d.selected);
			d3.select(this).classed('btn-default', !d.selected);
		});
};