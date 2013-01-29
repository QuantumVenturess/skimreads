$(document).ready(function() {
	$('.lazy').lazyload({
		failure_limit: 50,
        skip_invisible : false
	})
	$('.lazyLoad').lazyload({
		event: 'load',
		failure_limit: 50
	})
})