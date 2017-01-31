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
			chartArea: { left:'10%' },
			title: 'Runtime of tests on ',
			legend: { position: 'none' },
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
				viewWindowMode: 'maximized',
			},
			// Use an HTML tooltip.
			tooltip: { isHtml: true }			
		};
		var div_id = "chart_div_" + "hist";
		var str = '<div id="' + div_id + '" style="height:50%;width:90%"></div>';
		console.log(str);
		$('#charts').append(str);
		var chart = new google.visualization.Histogram(document.getElementById(div_id));
		chart.draw(data, options);
		
		google.visualization.events.addListener(chart, 'select', function() {
			alert('selected');
			var selection = chart.getSelection()[0];
			console.log(selection);
			console.log(selection.row);
			console.log(selection.column);
			console.log(data);
			console.log(data.getFormattedValue(selection.column - 1, selection.column - 1));
		});
	}
}