<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />
<%namespace file="../comment/funcs.mako" import="*" />

<%block name="title">Upload</%block>
<%block name="header">Upload</%block>

<%def name="up_file()">
	<table>
		<tr>
			<td><input type="file" name="file" size="16" onchange="$('#tags').val($('#default-tags').val())"></td>
			<td><input type="text" name="tags" id="tags"></td>
		</tr>
	</table>
</%def>

<%def name="up_data()">
	<table class="drop">
		<tbody class="msg-tbody">
			<tr><td colspan="2"><div class="msg">
				Drop files here to upload
				<br>Enter common tags in the box at the top
				<br>Enter any image-specific tags in the box next to each image
			</div></td></tr>
		</tbody>
	</table>
</%def>

<section id="upload">
	<h3>Upload</h3>
	<div>
		<form action="${route_path('posts')}" method="POST" enctype="multipart/form-data">
			<table style="width: 100%;">
				<tr>
					<td>
						<input id="default-tags" type="text" placeholder="Enter tags common to all images" class="shm-ac-tags" autocomplete="off">
					</td>
				</tr>
				<tr><td><hr/></td></hr>
				<tr>
					<td>${up_data()}</td>
				</tr>
				<tr><td><hr/></td></hr>
				<tr>
					<td>
						<input type="button" onclick="uploadAll();" value="Post All">
					</td>
				</tr>
			</table>
		</form>
	</div>
</section>
