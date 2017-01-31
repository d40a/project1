$(document).ready(function () {
	$("#btn_submit").click(function (e) {
		console.log('Clicked!');

		e.preventDefault();
		$('#charts').empty();

		function getData(url, args) {
			$.get(url, args, function (data) {
				var clChart = new columnChart();
				clChart.runDrawingChart(data.tests, args.os);
			});
		}

		// Send AJAX request for each selected OS
		$('#os_checboxes input:checked').each(function () {
			var os = $(this).attr('name');
			getData(
				window.location.href + "get_data/", 
				{
					test_suit: $("#test_suit").val(),
					tasks_limit: $("#tasks_limit").val(),
					os: os,
				}
			);
		});
	});
});