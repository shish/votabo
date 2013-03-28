<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${page.title}</%block>
<%block name="header">${page.title}</%block>
<%block name="nav">
	<section>
		<h3>Wiki Index</h3>
		<div>
			${render_bbcode(index.body)}
		</div>
	</section>
</%block>

<style>
.wiki-page TEXTAREA {
	width: 100%;
	height: 400px;
}
.wiki-page INPUT {
	width: 100%;
}
</style>

<section>
	<h3>${page.title} (r${page.revision} - ${render_date(page.posted)} - ${page.user.username})</h3>
	<div class="wiki-page">
		${form.errorlist("title")}
		${form.errorlist("body")}
		<form action="${route_url("wiki", title=page.title)}" method="POST">
			<input type="hidden" name="_method" value="PUT">
			<input type="hidden" name="title" value="${page.title}">
			<textarea name="body">${page.body}</textarea>
			<input type="submit" value="Save">
		</form>
	</div>
</section>
