if (typeof String.prototype.startsWith != 'function') {
	String.prototype.startsWith = function (str){
		return this.slice(0, str.length) == str;
	};
}

if (typeof String.prototype.endsWith != 'function') {
	String.prototype.endsWith = function (str){
		return this.slice(-str.length) == str;
	};
}

function magic(root) {
	root.find("time").timeago();
	
	root.find(".shm-ac-tags").tagit({
		fieldName: "tags",
		singleFieldDelimiter: " ",
		placeholder: "Tags",
		autocomplete: {delay: 0, minLength: 3},
		tagSource: function( request, response ) {
			var negative = request.term.startsWith("-");
			var negger = "";
			if(negative) {
				request.term = request.term.slice(1, request.term.length);
				negger = "-";
			}
			$.ajax({
				url: "/tags", 
				data: {
					starts_with: request.term
				},
				dataType: "json",
				success: function( data ) {
					response( $.map( data.tags, function( item ) {
						return {
							label: negger + item.name + " (" + item.count + ")",
							value: negger + item.name
						}
					}));
				}
			});
		},
	});
}

$(function() {
	magic($("BODY"));
	
	$(".jsHook-unlockOnChange").each(function(i, el) {
		$($(el).data("unlock")).prop('disabled', true);
	});
	$(".jsHook-unlockOnChange").keyup(function(evt) {
		$($(this).data("unlock")).prop('disabled', $(this).val().length == 0);
	});
});
