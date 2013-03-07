<%!
from webhelpers.text import truncate
%>
<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />
<%namespace file="../pm/funcs.mako" import="*" />

<%block name="title">${duser.username}</%block>
<%block name="header">${duser.username}</%block>
<%block name="nav">
	${parent.nav()}

	<section>
		<h3>Comments</h3>
		% for comment in duser.comments[:10]:
			<div class="comment">
				${render_bbcode(truncate(comment.body.replace("\n", " ").replace("\r", " "), 100, whole_word=True))}
				<a href="${route_path('post', id=comment.post_id)}">&gt;&gt;&gt;</a>
			</div>
		% endfor
	</section>
</%block>

<section>
	<h3>User Details: ${duser.username}</h3>
	<div style="text-align: center;">
		${render_avatar(duser)}
		<br>Joined: ${render_date(duser.joindate)}
		<br><a href="${route_path('posts', _query={'q': 'poster='+duser.username})}">Posts</a>: ${duser.post_count}
		<br><a href="${route_path('comments', _query={'q': 'poster='+duser.username})}">Comments</a>: ${duser.comment_count}
		<br>Category: ${duser.category}
		<br>User ID: ${duser.id}
	</div>
</section>

% if request.user:
	% if duser.username == request.user.username:  # FIXME: or has_permission('read-other-pm')
		${render_pm_list(duser, onlyUnread=True)}
	% endif
	% if duser.username != request.user.username:
		${render_pm_composer(duser)}
	% endif
% endif

<section>
	<h3>Recent Posts</h3>
	% for post in duser.posts[:12]:
		${render_thumb(post)}
	% endfor
	${render_thumbfiller()}
</section>
