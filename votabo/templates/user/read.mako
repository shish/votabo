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
	<div>
		<table><tr>
			<td>
				${render_avatar(duser)}
				<br>Joined: ${render_date(duser.joindate)}
				<br><a href="${route_path('posts', _query={'q': 'poster='+duser.username})}">Posts</a>: ${duser.post_count}
				<br><a href="${route_path('comments', _query={'q': 'poster='+duser.username})}">Comments</a>: ${duser.comment_count}
				<br>Category: ${duser.category}
				<br>User ID: ${duser.id}
			</td>
			% if has_permission("edit-user"):
			<td>
				<form action="${route_path('user', name=duser.username)}" method="POST">
					<table class="form">
						<tr>
							<td>Current Password:</td>
							<td><input type="password" name="current_password"></td>
						</tr>
						<tr>
							<td>Email:</td>
							<td><input type="text" name="email" value="${duser.email or ''}"></td>
						</tr>
						<tr>
							<td>New Password:</td>
							<td><input type="password" name="new_password_1"></td>
						</tr>
						<tr>
							<td>New Password (Repeat):</td>
							<td><input type="password" name="new_password_2"></td>
						</tr>
						<tr>
							<td colspan="2"><input type="submit" value="Save"></td>
						</tr>
					</table>
				</form>
			</td>
			% endif
		</tr></table>
	</div>
</section>

% if request.user:
	## FIXME: has_permission('read-pm')
	% if duser.username == request.user.username:  # FIXME: or has_permission('read-other-pm')
		${render_pm_list(duser, onlyUnread=True)}
	% endif
	## FIXME: has_permission('write-pm')
	% if duser.username != request.user.username:
		${render_pm_composer(duser)}
	% endif
% endif

% if duser.username == request.user.username:  # FIXME: or has_permission('change-other-setting')
<section>
	<h3>Options</h3>
	<div>
		<form action="${route_path('user', name=duser.username)}" method="PUT">
			<table class="form" style="margin: auto;">
				<thead>
					<tr><th colspan="2">Enter Current Password to Change Settings</th></tr>
				</thead>
				<tbody>
					<tr><th>Current Password</th><td><input type="password" name="password" class="jsHook-unlockOnChange" data-unlock=".user-option"></td></tr>
				</tbody>
				
				<tr><th colspan="2">&nbsp;</th></tr>

				<thead>
					<tr><th colspan="2">Change Password</th></tr>
				</thead>
				<tbody>
					<tr><th>New&nbsp;Password</th><td><input type="password" name="pass1" class="user-option"></td></tr>
					<tr><th>Repeat&nbsp;New&nbsp;Password</th><td><input type="password" name="pass2" class="user-option"></td></tr>
				</tbody>
				
				<tr><th colspan="2">&nbsp;</th></tr>
				
				<thead>
					<tr><th colspan="2">Change Email</th></tr>
				</thead>
				<tbody>
					<tr><th>Address</th><td><input type="text" name="email" value="${duser.email}" class="user-option"></td></tr>
				</tbody>
				
				<tr><th colspan="2">&nbsp;</th></tr>
				
				<tbody>
					<tr><td colspan="2"><input type="submit" value="Save All" class="user-option"></td></tr>
				</tbody>
			</table>
			
		</form>
	</div>
</section>
% endif

<section>
	<h3>Recent Posts</h3>
	% for post in duser.posts[:12]:
		${render_thumb(post)}
	% endfor
	${render_thumbfiller()}
</section>
