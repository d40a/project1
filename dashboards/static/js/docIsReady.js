$(document).ready(function () {
	
	function showPartition(partition) {
		$('#list_of_buckets').empty();
		partition = partition.sort(function(a,b){return a - b});
 
		for (var i = 0; i < partition.length; i++) {
			var innerHtml = partition[i].toString() 
				+ ' ms.'
			 	+ '<button type="button" class="btn btn-danger pull-right" name="btn_delete_perent">'
			    + '<span class="glyphicon glyphicon-remove"></span>';
		
			var li = new Tag({
					'tag': ['li'],
					'class': ['list-group-item', 'clearfix'],
					'value': [partition[i].toString()],
				},
				innerHtml
			);
			$("#list_of_buckets").append(li.html);
		}
		
		$('[name=btn_delete_perent]').click(function(e) {
			$(this).parent().remove();
		});
	}
	
	// TODO: Usage of angularJS could make the life easier...
	var partition = columnChart.defaultPartition();
	
	$('#btn_add_bucket_size').click(function () {
		// TODO: Validate input - allow input only numbers
		var bucket_size = parseInt($('#bucket_size').val());
		
		$('#bucket_size').val("");
	 	
		if (!isNaN(bucket_size) && !partition.includes(bucket_size)) {
			partition.push(parseInt(bucket_size));
			showPartition(partition);
		}
	});
	
	showPartition(partition);
	
	
	function getPartitions() {
		var partition = [];
		$("#list_of_buckets li").each(function(idx, li) {
			partition.push(li.value)
		});
		return partition;
	}
	
	$("#btn_submit").click(function (e) {
		console.log('Clicked!');

		e.preventDefault();
		$('#charts').empty();

		function getData(url, args) {
			$.get(url, args, function (data) {
				partition = getPartitions();
				var clChart = new columnChart(partition);
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
	$('#test_suits').children('a').each(function() {
		this.addEventListener('click', function(e) {
			$('#test_suit').val(e.target.innerText);
		});
	});
});