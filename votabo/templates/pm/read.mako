<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />
<%namespace file="../pm/funcs.mako" import="*" />

<%block name="title">${pm.subject}</%block>
<%block name="header">${pm.subject}</%block>

<section>
	<h3>Message from ${pm.user_from.username}</h3>
	<div>
		${render_avatar(pm.user_from, float_left=True)}
		${pm.message}
		<div style="clear: both;"><!-- clear avatar --></div>
	</div>
</section>

${render_pm_composer(pm.user_from, subject=add_re(pm.subject))}
