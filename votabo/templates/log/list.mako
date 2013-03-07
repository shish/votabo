<%!
from datetime import datetime
from webhelpers.util import update_params
%>
<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${"Log Events"}</%block>
<%block name="header">${"Log Events"}</%block>

<section>
	<h3>Log Events</h3>
	<table class="small zebra">
		<thead>
			<tr>
				<th>Time</th>
				<th>Module</th>
				<th>Username</th>
				<th>IP</th>
				<th colspan="2">Message</th>
			</tr>
			<tr>
				<form action="${request.url}" method="GET">
					<td><input type="text" name="time" value="${request.GET.get('time', '')}" /></td>
					<td><input type="text" name="module" value="${request.GET.get('module', '')}" /></td>
					<td><input type="text" name="username" value="${request.GET.get('username', '')}" /></td>
					<td><input type="text" name="address" value="${request.GET.get('address', '')}" /></td>
					<td><input type="text" name="message" value="${request.GET.get('message', '')}" /></td>
					<td><input type="submit" value="Search" /></td>
				</form>
			</tr>
		</thead>
		<tbody>
			% for log in logs:
				<tr>
					<td style="white-space: nowrap;">${render_date(log.timestamp, raw=True)}</td>
					<td><a href="${update_params(request.url, module=log.section, page=1)}">${log.section}</a></td>
					<td>${log.username}</td>
					<td><a href="${update_params(request.url, address=log.address, page=1)}">${log.address}</a></td>
					<td colspan="2">${log.message}</td>
				</tr>
			% endfor
		</tbody>
	</table>
</section>
