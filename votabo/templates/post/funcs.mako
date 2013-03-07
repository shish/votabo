<%def name="upload_block_small()">
	<section>
		<h3>Quick Upload</h3>
		<div>
			<div class="mini_upload">
				<form action="${route_path('posts')}" method="POST" enctype="multipart/form-data">
					<input name="file" size="16" type="file" multiple="multiple" required="required">
					<input name="tags" type="text" placeholder="tagme" class="shm-ac-tags" required="required">
					<input type="submit" value="Post">
				</form>
				<a href="${route_path('posts/upload')}">Full Uploader</a>
			</div>
		</div>
	</section>
</%def>
