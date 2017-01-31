function prepairDataForHistogram(buckets) {
	var result = [['Name of test', 'Runtime of test']];
	for (var key in buckets) {
		var listOfTests = buckets[key];
		for (var i in listOfTests) {
			var test = listOfTests[i];
			for (var task_id in test.dict_task_id_to_runtime) {
				result.push([test.name, test.dict_task_id_to_runtime[task_id]]);
			}
		}
	}
	return result;
}

function drawHistogram(results) {

	google.charts.load("current", {packages: ["corechart"]});
	google.charts.setOnLoadCallback(drawChart);

	function drawChart() {
		var data = google.visualization.arrayToDataTable(
			results
		);

		var options = {
			title: 'Runtime of tests on ',
			legend: {
				position: 'none'
			},
			explorer: {
				actions: ['dragToZoom', 'rightClickToReset'], 
				maxZoomIn: 25,
			},
			vAxis: { 
				title: 'number of tests',
				scaleType: 'mirrorLog',

			},
			hAxis: {
				title: 'time in ms',
				viewWindowMode: 'explicit',
			}

		};
		var div_id = "chart_div_" + "hist";
		var str = '<div id="' + div_id + '"></div>';
		console.log(str);
		$('#charts').append(str);
		var chart = new google.visualization.Histogram(document.getElementById(div_id));
		chart.draw(data, options);
	}
}