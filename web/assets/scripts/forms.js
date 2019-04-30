$.fn.select2.defaults.set("theme", "bootstrap4");

$(window).on('load', function () {
	$('select').select2({
		ajax: {
			url: function (params) {
				return window.location;
			},
			data: function (params) {
				return {
					search: params.term,
					type: $(this).attr('name'),
					page: params.page || 1
				};
			},
			processResults: function (data, params) {
				return {
					results: data.items,
					pagination: {
						more: data.pagination.more
					}
				}
			},
		},
	});
});
