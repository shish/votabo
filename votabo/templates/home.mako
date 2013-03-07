<html>
	<head>
		<script src="${static_url('js/vendor/jquery-1.9.0.min.js')}"></script>
		<style>
.dropzone .files {
	width: 400px;
	height: 200px;
	border: 1px solid black;
}
		</style>
		<script>
$(function() {
jQuery.event.props.push('dataTransfer');
	var dataArray = [];
	$(".files").bind('drop', function(e) {
		var files = e.dataTransfer.files;
		$.each(files, function(index, file) {
			if (!files[index].type.match('image.*')) {
				alert("images only");
				return false;
			}

			var fileReader = new FileReader();
			fileReader.onload = (function(file) {
				return function(e) { 
					dataArray.push({name : file.name, value : this.result});
					var image = this.result;
					$(".files").append('<img src="'+image+'" style="max-width: 100px; max-height: 100px;">');
					$(".files").append('<input type="hidden" name="data" value="'+image+'">');
				};
			})(files[index]);
			fileReader.readAsDataURL(file);
		});
		return false;
	});
});
		</script>
	</head>
	<body>
		<form action="/file-upload" class="dropzone" id="my-awesome-dropzone">
			<div class="files" ondragover="return false;">
				Drop files here
			</div>
			<input type="text" name="tags">
			<input type="submit">
		</form>
	</body>
</html>
