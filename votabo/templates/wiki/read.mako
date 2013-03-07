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

<section>
	<h3>${page.title} (r${page.revision} - ${render_date(page.posted)} - ${page.user.username})</h3>
	<div class="wiki-page">
		${render_bbcode(page.body)}
	</div>
</section>
