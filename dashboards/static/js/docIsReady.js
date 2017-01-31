$(document).ready(function () {
	$("#btn_submit").click(function (e) {
		console.log('Clicked!');
		console.log('ASDASDS');
		e.preventDefault();
		$('#charts').empty();

		function getData(url, args) {
			$.get(url, args, function (data) {
				console.log(data);

//				promptDrawingChart(data['buckets'], args['os']);
				drawHistogram(prepairDataForHistogram(data.buckets));
			});
		}

//  	Send AJAX request for each selected OS
		$('#os_checboxes input:checked').each(function () {
			var os = $(this).attr('name');
			getData(
				window.location.href + "get_data/", {
					test_suit: $("#test_suit").val(),
					tasks_limit: $("#tasks_limit").val(),
					os: os,
				}
			);
		});
	});
});