(function($) {

	let options = {
		events_source: "/activity/ajax/get_data",
		view: 'month',
		tmpl_path: '/activity/ajax/get_template/',
		// tmpl_cache: false,
		// day: '2013-03-12',
		language: 'zh-CN',
		onAfterEventsLoad: function(events) {
			if(!events) {
				return;
			}
			let list = $('#eventlist');
			list.html('');

			$.each(events, function(key, val) {
				$(document.createElement('li'))
					.html('<a href="' + val.url + '">' + val.title + '</a>')
					.appendTo(list);
			});
		},
		onAfterViewLoad: function(view) {
			$('.page-header .this-month').text(this.getTitle());
			$('.btn-group button').removeClass('active');
			$('button[data-calendar-view="' + view + '"]').addClass('active');
		},
		classes: {
			months: {
				general: 'label'
			}
		}
	};

	let calendar = $('#calendar').calendar(options);

	$('.btn-group button[data-calendar-nav]').each(function() {
		let $this = $(this);
		$this.click(function() {
			calendar.navigate($this.data('calendar-nav'));
		});
	});

	$('.btn-group button[data-calendar-view]').each(function() {
		let $this = $(this);
		$this.click(function() {
			calendar.view($this.data('calendar-view'));
		});
	});
}(jQuery));