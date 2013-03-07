<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${query or "All Comments"}</%block>
<%block name="header">${query or "All Comments"}</%block>

% for comment in comments:
	${render_thread(comment.post)}
% endfor

<section id="paginator">
	${comments.pager("$link_previous ~3~ $link_next")}
</section>
