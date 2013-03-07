$(function() {
	jQuery.event.props.push('dataTransfer');

    $(".drop").bind('dragover', function(e, el) {
		$(this).css('background', '#7EB977');
		return false;
	});
    $(".drop").bind('dragleave', function(e, el) {
		$(this).css('background', '');
		return false;
	});

    var dataArray = [];
    $(".drop").bind('drop', function(e, el) {
		$(this).css('background', '');

        var files = e.dataTransfer.files;
        $.each(files, function(index, file) {
            if(!files[index].type.match('image/.*')) {
                alert("images only");
                return false;
            }

            var fileReader = new FileReader();
            fileReader.onload = (function(file) {
                return function(e) {
                    dataArray.push({name : file.name, value : this.result});
                    var image = this.result;
					var tbody = $('<tbody>');
					tbody.append($('<tr><td rowspan="3"><img class="upthumb" src="'+image+'">'+
					               '<div class="progress"><div class="bar"></div></div>'+
					               '<input type="hidden" class="data" name="data" value="'+image+'" />'+
					               '<input type="hidden" class="mimetype" name="mimetype" value="'+file.type+'" />'+
								   '</td>'+
                                   '<td style="width: 100%;"><input type="text" class="filename" name="filename" value="'+file.name+'"></td></tr>'));
					tbody.append($('<tr><td><input type="text" class="tags shm-ac-tags" name="tags" placeholder="Enter extra tags"></td></tr>'));
					tbody.append($('<tr><td><input type="button" class="button" onclick="upload($(this).parent().parent().parent());" value="Post"></td></tr>'));
					tbody.append($('<tr><td colspan="2"><hr /></td></tr>'));
					$(".msg-tbody").before(tbody);
					magic(tbody);
                };
            })(files[index]);
            fileReader.readAsDataURL(file);
        });
        return false;
    });
});

function upload(tbody) {
	tbody.find(".filename").prop("disabled", true);
	tbody.find(".tags").prop("disabled", true);
	tbody.find(".button").prop("disabled", true);

	tbody.find(".button").val("Uploading ...");
	tbody.find(".tags").val($("#default-tags").val() + " " + tbody.find(".tags").val());

	var formdata = {
		"filename": tbody.find(".filename").val(),
		"mimetype": tbody.find(".mimetype").val(),
		"tags": tbody.find(".tags").val() + " " + $("#default-tags").val(),
		"data": tbody.find(".data").val()
	};

	$.ajax({
		url: '/post',
		type: 'POST',
		data: formdata,
		xhr: function() {
			var xhr = jQuery.ajaxSettings.xhr();
			if(xhr instanceof window.XMLHttpRequest) {
				function on_progress(progress) {
					if(progress.lengthComputable) {
						tbody.find(".button").val("Uploading ... ("+Math.floor(progress.loaded/1024)+"/"+Math.floor(progress.total/1024)+" KB)");
						tbody.find(".progress .bar").width((progress.loaded / progress.total * 100) + "%");
					}
				};
				xhr.upload.addEventListener('progress', on_progress, false);
				//xhr.upload.addEventListener('load', on_loaded, false);
				//xhr.addEventListener('abort', on_abort, false);
			}
			return xhr;
		},
		success: function(e) {
			tbody.find(".button").val("Success");
			tbody.find(".progress .bar").width("100%");
		},
		error: function(e) {
			tbody.find(".filename").prop("disabled", false);
			tbody.find(".tags").prop("disabled", false);
			tbody.find(".button").prop("disabled", false);
			tbody.find(".button").val("Unknown Error (Click to try again)");
			tbody.find(".progress .bar").width("100%");
			tbody.find(".progress .bar").css("background", "red");
		},
	});
}

function uploadAll() {
	$(".drop").children().each(function(i, el) {
		if($(el).find(".filename").length == 1) {
			upload($(el));
		}
	});
}
