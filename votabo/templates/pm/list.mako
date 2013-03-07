<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />
<%namespace file="../pm/funcs.mako" import="*" />

<%block name="title">PM List</%block>
<%block name="header">PM List</%block>

% if request.user:
	${render_pm_list(request.user)}
% endif
