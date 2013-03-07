<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${starts_with or "All Tags"}</%block>
<%block name="header">${starts_with or "All Tags"}</%block>

<section>
	<h3>Tags</h3>
	<div>
		% for letter in "abcdefghijklmnopqrstuvwxyz?":
			<a href="${route_path('tags', _query={'starts_with': letter})}">${letter.upper()}</a>
		% endfor
		<hr>
		% for tag in tags:
			${render_tag(tag, scaled=True)}
		% endfor
	</div>
</section>
