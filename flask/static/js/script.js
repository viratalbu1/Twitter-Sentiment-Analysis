$(document).ready(function(){
	var ctx = $("#mycanvas").get(0).getContext("2d");

	var data = [
		{
			value: 290,
			color: "cornflowerblue",
			highlight: "lightskyblue",
			label: "Javt"
		},
		{
			value: 30,
			color: "lightgreen",
			highlight: "yellowgreen",
			label: "HTML"
		},
		{
			value: 40,
			color: "orange",
			highlight: "darkorange",
			label: "SS"
		}
	];

	var chart = new Chart(ctx).Doughnut(data);
});