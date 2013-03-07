$(function() {
	$(".shm-zoomer").change(function(e) {
		zoom(this.options[this.selectedIndex].value);
	});

	$($(".shm-zoomer").data("target")).click(function(e) {
		switch($.cookie("ui-image-zoom")) {
			case "full": zoom("width"); break;
			default: zoom("full"); break;
		}
	});

	if($.cookie("ui-image-zoom")) {
		zoom($.cookie("ui-image-zoom"));
	}
});

function zoom(zoom) {
	var img = $($(".shm-zoomer").data("target"));

	img.css('max-width', '');
	img.css('max-height', '');
	if(zoom == "width" || zoom == "both") {
		img.css('max-width', '100%');
	}
	if(zoom == "height" || zoom == "both") {
		img.css('max-height', (window.innerHeight * 0.95) + 'px');
	}

	$(".shm-zoomer").val(zoom);

	$.cookie("ui-image-zoom", zoom, {path: '/', expires: 365});
}
