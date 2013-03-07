function magic(root) {
	root.find("time").timeago();
	root.find(".shm-ac-tags").tagit({
		fieldName: "tags",
		singleFieldDelimiter: " ",
		placeholder: "Tags",
		autocomplete: {delay: 0, minLength: 3},
		tagSource: function( request, response ) {
			$.ajax({
				url: "/tags", 
				data: { starts_with: request.term },
				dataType: "json",
				success: function( data ) {
					response( $.map( data.tags, function( item ) {
						return {
							label: item.name + " (" + item.count + ")",
							value: item.name
						}
					}));
				}
			});
		},
	});
}

$(function() {
	magic($("BODY"));
});
