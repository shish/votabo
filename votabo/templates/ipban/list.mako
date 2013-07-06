<%!
from datetime import datetime
%>
<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${"IP Bans"}</%block>
<%block name="header">${"IP Bans"}</%block>

<section>
	<h3>IP Bans</h3>
	<table class="small zebra">
		<thead>
			<tr>
				<th>IP</th>
				<th>Reason</th>
				<th>By</th>
				<th>Added</th>
				<th>Until</th>
				<th>Action</th>
			</tr>
			<tr>
				<form action="${request.url}" method="GET">
					<td><input type="text" name="ip" value="${request.GET.get('ip', '')}" /></td>
					<td><input type="text" name="reason" value="${request.GET.get('reason', '')}" /></td>
					<td><input type="text" name="banner" value="${request.GET.get('banner', '')}" /></td>
					<td></td>
					<td></td>
					<td><input type="submit" value="Search" /></td>
				</form>
			</tr>
		</thead>
		<tbody>
			% for ban in ipbans:
				<tr>
					<td>${ban.ip}</td>
					<td>${ban.reason}</td>
					<td>${render_username(ban.banner)}</td>
					<td style="white-space: nowrap;">${render_date(ban.added, raw=True, time=False)}</td>
					<td style="white-space: nowrap;">${render_date(datetime.fromtimestamp(ban.until), raw=True, time=False)}</td>
					<form action="${route_path('ipban', id=ban.id)}" method="POST">
						<td>
							<input type="hidden" name="_method" value="DELETE" />
							<input type="submit" value="Remove" />
						</td>
					</form>
				</tr>
			% endfor
		</tbody>
	</table>
</section>
