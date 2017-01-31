function promptDrawingChart(frequency_on_intervals, bot_os) {
	console.log(frequency_on_intervals);
	var arr_frequency_on_intervals = [['runtime ms', 'number of tests']];
	for (var interval in frequency_on_intervals) {
		var arr_item = [];
		arr_item.push(interval, frequency_on_intervals[interval]);
		arr_frequency_on_intervals.push(arr_item);
	}
	console.log(arr_frequency_on_intervals);
	google.charts.load("current", {
		packages: ["corechart"]
	});
	google.charts.setOnLoadCallback(drawChart);

	function drawChart() {
		var data = google.visualization.arrayToDataTable(
			arr_frequency_on_intervals
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