export const render = (canvasId, payload) => {
	var canvas = document.getElementById(canvasId);
	var ctx = canvas.getContext('2d');
	var myChart = new Chart(ctx, {
		type: canvas.dataset.chartType,
		data: payload.data,
		options: payload.options
	});
};

export const reload = (canvasId, url) => {
	fetch(url, {
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
			'Accept': 'application/json'
		},
		credentials: 'include'
	})
		.then(function (response) {
			return response.json();
		})
		.then(function (data) {
			render(canvasId, data);
		})
};
