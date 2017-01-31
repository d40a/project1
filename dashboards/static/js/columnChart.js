function columnChart() { 
	var buckets;
	var partition;
	// return sizes of backets - logarithmic scale
	function defaultPartition() {
		var partition = [1];
		var base = 10;
		for (var i = 0; i < 7; i++) {
			partition.push(base);
			base *= 10;
		}
		return partition;
	};

	function fillBuckets(tests, partition) {
		console.log(tests);
		buckets = new Array(partition.length + 1);
		for (var i = 0; i < buckets.length; i++) {
			buckets[i] = new Array();
		}
		console.log(buckets);
		console.log(partition.length);
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
			console.log(buckets[i].length)
			if (buckets[i].length == 0) buckets.pop();
			else break;
		}
		return buckets;
	};

	function prepairDataForColumnChart(dataFromServer) {
		var dataForColumnChart = [['Number tests in bucket', "Test's runtime"]];
		partition = defaultPartition();
		buckets = fillBuckets(dataFromServer, partition);

		for (var i = 0; i < buckets.length - 1; i++) {
			dataForColumnChart.push([" < " + partition[i].toString(), buckets[i].length]);
		}

		dataForColumnChart.push(['Rest', buckets[buckets.length - 1].length]);
		return dataForColumnChart;
	};

	function DivTag(attributes) {
		var tag = '<div';
		for (var key in attributes) {
			tag += " " + key + '="' + attributes[key] + '"';
		}
		tag += '></div>'
		this.tag = tag;
		this.attributes = attributes;
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
	
			var div = new DivTag({
				'id': 'basic_column_chart_' + bot_os,
				'style': 'height: 700px;background-color:lavender;',
				'class': 'col-md-6',
			});

			$('#charts').append(div.tag);

			var chart = new google.visualization.ColumnChart(document.getElementById(div.attributes.id));
			chart.draw(data, options);

			google.visualization.events.addListener(chart, 'select', function () {
				var selection = chart.getSelection();
				// selection structure: 
				// Array[1]
				//  0:Object
				// 	 column:1
				//   row:1

				if (selection.length > 0) {
					var row = selection[0].row;
					printTestsFromBucket(row, div);
				}
			});
		}
	};



	this.printTestsFromBucket = function(bucketsIndex, div) {
		for (var i = 0; i < buckets[bucketsIndex].length; i++) {
			var test = buckets[bucketsIndex][i];
			console.log(JSON.stringify(test));
		}
	}
}