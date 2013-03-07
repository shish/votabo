<%!
from datetime import datetime
%>
<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${"User List"}</%block>
<%block name="header">${"User List"}</%block>

<section>
	<h3>User List</h3>
	<table class="zebra">
		<thead>
			<tr>
				<th>ID</th>
				<th>Username</th>
				<th>Posts</th>
				<th>Comments</th>
				<th>Category</th>
				<th>Action</th>
			</tr>
			<tr>
				<form action="${request.url}" method="GET">
					<td><input type="text" name="id" value="${request.GET.get('id', '')}" /></td>
					<td><input type="text" name="username" value="${request.GET.get('username', '')}" /></td>
					<td><input type="checkbox" name="posts" ${'checked="checked"' if request.GET.get('posts') else ''}></td>
					<td><input type="checkbox" name="comments" ${'checked="checked"' if request.GET.get('comments') else ''}></td>
					<td><input type="text" name="category" value="${request.GET.get('category', '')}" /></td>
					<td><input type="submit" value="Search" /></td>
				</form>
			</tr>
		</thead>
		<tbody>
			% for duser in users:
				<tr>
					<td>${duser.id}</td>
					<td>${render_username(duser)}</td>
					<td><a href="${route_path('posts', _query={'q': 'poster='+duser.username})}">${duser.post_count}</a></td>
					<td><a href="${route_path('comments', _query={'q': 'poster='+duser.username})}">${duser.comment_count}</a></td>
					<td>${duser.category}</td>
					<td></td>
				</tr>
			% endfor
		</tbody>
	</table>
</section>
