<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${starts_with or "All Tags"}</%block>
<%block name="header">${starts_with or "All Tags"}</%block>

<section id="tag_map">
	<h3>Tags</h3>
	<div>
		% for letter in "abcdefghijklmnopqrstuvwxyz?":
			<a href="${route_path('tags', _query={'starts_with': letter})}">${letter.upper()}</a>
		% endfor
			<br>&nbsp;
			<form class="searchbutton">
				<input type="hidden" name="starts_with" value="">
				<table class="search"><tr><td width="80%">
					<input type="text" placeholder="search for partial tag" name="contains" value="${request.GET.get('contains', '')}">
				</td><td>
					<input type="submit" value="Search">
				</td></tr></table>
			</form>
		<hr>
		% for tag in tags:
			${render_tag(tag, scaled=True)}
		% endfor
	</div>
</section>
