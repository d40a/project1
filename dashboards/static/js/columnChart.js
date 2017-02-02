function columnChart(partition) { 
	var buckets;

	function fillBuckets(tests, partition) {
 		buckets = new Array(partition.length + 1);
		for (var i = 0; i < buckets.length; i++) {
			buckets[i] = new Array();
		}
 
		for (var i = 0; i < tests.length; i++) {
			var test = tests[i];
			// looking for first number that is larger than test.runtime
			var j = 0;
			for (; j < partition.length; j++) {
				if (test.runtime <= partition[j]) {
					break;
				}
			}
			// j == partition.len + 1 when there is not exist number larger than test.runtime
			buckets[j].push(test);
		}

		// remove empty tail elements
		for (var i = buckets.length - 1; i >= 0; i--) {
			if (buckets[i].length == 0) buckets.pop();
			else break;
		}
		return buckets;
	};

	function prepairDataForColumnChart(dataFromServer) {
		var dataForColumnChart = [['Number tests in bucket', "Test's runtime"]];
		buckets = fillBuckets(dataFromServer, partition);

		for (var i = 0; i < buckets.length; i++) {
            // it is possible to have smaller number of buckets because we cleaned up empty ones on in the tail
            if (i < partition.length) {
                dataForColumnChart.push([" < " + partition[i].toString(), buckets[i].length]);
            }
            else {
                dataForColumnChart.push(['Rest', buckets[buckets.length - 1].length]);
            }
		}
		return dataForColumnChart;
	};
	


	this.runDrawingChart = function(tests, bot_os='default bot') {
		
		var dataForColumnChart = prepairDataForColumnChart(tests);

		google.charts.load("current", {	packages: ["corechart"] });
		google.charts.setOnLoadCallback(drawChart);

		function drawChart() {
			var data = google.visualization.arrayToDataTable(
				dataForColumnChart
			);

			var options = {
				title: 'Runtime of tests on ' + bot_os,
				legend: {
					position: 'none'
				},
				explorer: {
					actions: ['dragToZoom', 'rightClickToReset'], 
					maxZoomIn: 25,
				},
				hAxis: {
					title: 'time in ms.',
				},
				vAxis: {
					title: 'number of tests',
				},
			};
			
			var div = new Tag({
				'tag': ['div'],
				'id': ['basic_column_chart_' + bot_os],
				'style': ['max-height:70%;', 'height:70%;', 'overflow:auto;'],
				'class': ['col-md-6'],
			});
			
			var wrapperDiv = new Tag({
				'tag': ['div'],
				'id': ['wrapper_' + div.attributes.id],
				'class': ['col-md-12'],
				'style': ['max-height:70%;'],
			});
			
			$('#charts')
				.append(wrapperDiv.html);
			$('#' + wrapperDiv.attributes.id)
				.append(div.html);
			
			var chart = new google.visualization.ColumnChart(document.getElementById(div.attributes.id));
			chart.draw(data, options);

			google.visualization.events.addListener(chart, 'select', function () {
				var selection = chart.getSelection();
				$('#' + div.attributes.id).next().remove();
				if (selection.length > 0) {
					var row = selection[0].row; // getting number of selected row
					printTestsFromBucket(row, div);
				}
			});
			console.log(cnt_comming_responces);
			cnt_comming_responces -= 1;
		}
	};

	// TODO: Delete previous list of test for the same dashboard (each list of tests div will have unique id that we can easily build knowing div_id)
	function printTestsFromBucket(bucketsIndex, div) {
		var tests = buckets[bucketsIndex].sort(function(a, b) {
			return -(a.runtime - b.runtime);		
		});
		var commonSuffixForIds = bucketsIndex.toString() + '_' + div.attributes.id;
		
		var list_of_tests_div = new Tag({
			'tag': ['div'],
			'id': ['div_list_' + commonSuffixForIds], 
			'class': ['col-md-6'],
			'style': ['overflow:auto;', 'max-height:70%;'],
		});
		
		var uList = new Tag({
			'tag': ['ul'],
			'id': ['list_' + commonSuffixForIds], 
			'class': ['list-group'],
		});
		
		$('#' + div.attributes.id)
			.after(list_of_tests_div.html);
		
		$('#' + list_of_tests_div.attributes.id)
			.append(uList.html);
		
		for (var i = 0; i < tests.length; i++) {
			var test = tests[i];
			var list_element = new Tag({
				'tag': ['li'],
				'class': ['list-group-item'],
			});
			
			function testToHtml(test) {
				var str = '<b>Test name: </b>' + test.name + '<br><b>Runtime: </b>' + test.runtime + 'ms <br><b>Task: </b>' + test.task_id;
				return str; 
			}
			
			$(list_element.html)
				.appendTo('#' + uList.attributes.id)
				.append(testToHtml(test));
		}
		
	}
}

// return sizes of backets - logarithmic scale
columnChart.defaultPartition = function() {
	var partition = [1];
	var base = 10;
	for (var i = 0; i < 6; i++) {
		partition.push(base);
		base *= 10;
	}
	return partition;
}
