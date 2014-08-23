<%namespace file="../common/funcs.mako" import="*" />
<%namespace module="votabo.lib.template_extras" import="*" />

<%def name="render_comment(comment)" cached="True" cache_timeout="120" cache_key="comment-${str(comment.id)}-${str(has_permission('comment-delete'))}">
	<div class="comment" id="c${comment.id}">
		<div class="info">
			${render_date(comment.posted)}
			<br><a href="javascript: replyTo(${comment.post_id}, ${comment.id}, ${comment.user.username});">Reply</a>
		</div>
		${render_username(comment.user)}:
		${render_bbcode(comment.body)}
	</div>
</%def>

<%def name="render_comment_box(post)">
	% if has_permission("comment-create"):
		<div class="comment">
			<form action="${route_path('comments')}" method="POST">
				<input type="hidden" name="image_id" value="${post.id}">
				<textarea id="comment_on_${post.id}" name="comment" rows="5"></textarea>
				<br><input type="submit" value="Post Comment">
			</form>
		</div>
	% endif
</%def>

<%def name="render_thread(post, limit=10)" cached="True" cache_timeout="30" cache_key="thread-${str(post.id)}-${str(limit)}">
	<section id="comment-list-list">
		<h3>${post.id}: ${post.title}</h3>
		<table><tr><td width="220">
			${render_thumb(post)}
		</td><td>
			<%
			allc = list(post.comments)
			%>
			% if len(allc) > limit:
				<p>showing ${limit} of ${len(allc)} comments</p>
			% endif
			% for comment in allc[-limit:]:
				${render_comment(comment)}
			% endfor
			${render_comment_box(post)}
		</td></tr></table>
	</section>
</%def>
