$(document).ready(function() {
	$('.lazy').lazyload({
		effect: 'fadeIn',
		failure_limit: 50
	})
	$('.lazyLoad').lazyload({
		event: 'load',
		effect: 'fadeIn',
		failure_limit: 50
	})
})