<%!
import math
%>

<%def name="add_re(text)"><%
	if text.startswith("Re: "):
		return text
	else:
		return "Re: " + text
%></%def>

<%def name="render_autolink(text)">
	## TODO: add "a href=..." if text looks like a link
	% if text:
		<a href="${text}">${text}</a>
	% endif
</%def>

<%def name="render_date(date, raw=False, time=True)">
	% if raw:
		% if time:
			${date.strftime('%Y-%m-%d %H:%M')}
		% else:
			${date.strftime('%Y-%m-%d')}
		% endif
	% else:
		<time datetime="${date.strftime('%Y-%m-%dT%H:%M:%S%Z')}">${date.strftime("%Y-%m-%d %H:%M")}</time>
	% endif
</%def>

<%def name="render_tag(tag, block=False, scaled=False, count=False)">
	<%
	styles = []

	if scaled:
		size = math.floor(math.log1p(math.log1p(tag.count - tags_min)) * 1.5 * 100) / 100
		if size < 0.01:
	 		return ""
		styles.append("font-size: %.3fem" % size)

	if block:
		styles.append("display: inline-block;")
		styles.append("margin-right: 0.5em;")
	%>
    <a style="${' '.join(styles)}" href="${route_path('posts', _query={'q': tag.name})}" title="${tag.category}">${tag.name.replace("_", " ")}</a>
	% if count:
		(${tag.count})
	% endif
</%def>

<%def name="render_thumb(post, query=None)" cached="True" cache_timeout="120" cache_key="thumb-${str(post.id)}">
	<div class="shm-thumb thumb" data-tags="${post.tags_plain_text}"
		><a class="shm-thumb-link" href='${route_path("post", id=post.id)}'
			><img id="thumb_${post.id}" title="${post.tooltip}" height="${post.thumb_height}" width="${post.thumb_width}" src="${post.thumb_url}"
		></a>
		<br><a href="${post.image_url}">Image Only</a>
		<span class="need-image-delete">
			- <a href='#' onclick='image_hash_ban(${post.id}); return false;'>Ban</a>
		</span>
	</div>
</%def>

<%def name="render_thumbfiller()">
	## fill some space to trigger full-justify on the final line
	% for n in range(0, 8):
		<div style="width: 226px; height: 0px; display: inline-block;"></div>
	% endfor
</%def>

<%def name="render_username_str(username)" filter="trim">
	% if username == "Anonymous":  # FIXME don't hardcode
		<span class="username">${username}</span>
	% else:
		<a class="username" href="${route_path('user', name=username)}">${username}</a>
	% endif
</%def>
	
<%def name="render_username(user)" filter="trim">
	${render_username_str(user.username if user else 'None')}
</%def>

<%def name="render_avatar(user, size=80, float_left=False)" filter="trim">
	<a class="avatar" href="${route_path('user', name=user.username)}"
	${'style="float: left; margin-right: 8px; margin-bottom: 8px;"' if float_left else ''|n}
	><img src="${user.get_avatar_url(size)}" /></a>
</%def>

