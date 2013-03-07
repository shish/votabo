<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />
<%namespace file="../comment/funcs.mako" import="*" />

<%block name="title">${post.title}</%block>
<%block name="header">${post.title}</%block>
<%block name="bodyclass">post-read</%block>
<%block name="nav">
	${parent.nav()}
	<section>
		<h3>Tags</h3>
		<div>
			% for n, tag in enumerate(post.tags):
				% if n > 0:
					<br>
				% endif
				${render_tag(tag, count=True)}
			% endfor
		</div>
	</section>

	<section>
		<h3>Image Controls</h3>
		<div>
			<form>
				<select class="shm-zoomer" data-target=".shm-main-image">
					<option value="full">Full Size</option>
					<option value="width">Fit Width</option>
					<option value="height">Fit Height</option>
					<option value="both">Fit Both</option>
				</select>
			</form>
		</div>
	</section>
</%block>

<section>
	<h3>${post.title}</h3>
	<div class="blockbody">
		<img src="${post.image_url}" class="shm-main-image" data-width="${post.width}" data-height="${post.height}">
	</div>
	<div class="blockbody">
		<table class="post-info form">
			<tbody><tr>
				<th>Uploader</th>
				<td>
					<span class="view">${render_username(post.user)}, ${render_date(post.posted)}</span>
					<input class="edit" type="text" name="user" value="${post.user.username}">
				</td>
				<td width="80px" rowspan="4">${render_avatar(post.user)}</td>
			</tr>
			<tr>
				<th width="50px">Tags</th>
				<td>
					<input type="text" name="tags" value="${post.tags_plain_text}" class="shm-ac-tags" onfocus="$('.view').hide(); $('.edit').show();">
				</td>
			</tr>
			<tr>
				<th>Source</th>
				<td>
					<span class="view ellipsis">${render_autolink(post.source)}</span>
					<input class="edit" type="text" name="source" value="${post.source}">
				</td>
			</tr>
			<tr>
				<th>Locked</th>
				<td>
					<span class="view">${"Yes" if post.locked else "No"}</span>
					<input class="edit" type="checkbox" name="locked">
				</td>
			</tr>
			<tr><td colspan="4">
				<input class="view" type="button" value="Edit" onclick="$('.view').hide(); $('.edit').show();">
				<input class="edit" type="submit" value="Set">
			</td></tr>
		</tbody></table>
	</div>
</section>

<section>
	<h3>Comments</h3>
	% for comment in post.comments:
		${render_comment(comment)}
	% endfor
	${render_comment_box(post)}
</section>
