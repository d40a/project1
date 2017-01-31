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
	}
	
	function fillBuckets(tests, partition) {
		buckets = new Array(partition.length + 1);
		for (var test in tests) {
			var i = 0;
			// looking for first number that is larger than test.runtime
			for (; i < partition.length; i++) {
				if (test.runtime <= partition[i]) {
					break;
				}
			}
			// i == partition.len + 1 when there is not exist number larger than test.runtime
			buckets[i].push(test);
		}
		return buckets;
	}
	
	// TODO: SUPPORT OS
	function prepairDataForColumnChart(dataFromServer) {
		var dataForColumnChart = [['Number tests in bucket', "Test's runtime"]];
		partition = defaultPartition();
		buckets = fillBuckets(dataFromServer, partition);
		
		for (var i = 0; i < buckets.length - 1; i++) {
			dataForColumnChart.push([partition[i], buckets[i].length]);
		}
		
		dataForColumnChart.push(['Rest', buckets[buckets.length - 1].length]);
		return dataForColumnChart;
	}

	function runDrawingChart(dataForColumnChart, bot_os='default bot') {
		console.log('I am here');
		console.log(dataForColumnChart);
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
			};
			var div_id = "chart_div_" + bot_os;
			var str = '<div id="' + div_id + '" style="width: 1100px; height: 700px;"></div>';
			console.log(str);
			$('#charts').append(str);
			var chart = new google.visualization.ColumnChart(document.getElementById(div_id));
			chart.draw(data, options);

			google.visualization.events.addListener(chart, 'select', function () {
				var selection = chart.getSelection();
				console.log(selection);
			});
		}
	}
}