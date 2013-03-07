<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${query or "All Posts"}</%block>
<%block name="header">${query or "All Posts"}</%block>
<%block name="navblock_extra">
	<form action="${route_path('posts')}" method="GET">
		<input type="text" class="shm-ac-tags" name="q" placeholder="Enter Keywords" value="${request.GET.get('q', '')}">
	</form>
</%block>


<section id="image-list">
	<h3>Posts</h3>
	% if posts:
		% for post in posts:
			${render_thumb(post)}
		% endfor
		${render_thumbfiller()}
	% else:
		<div>
			No posts found :(
		</div>
	% endif
</section>
