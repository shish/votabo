<%!
from datetime import datetime
%>
<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${"Post Bans"}</%block>
<%block name="header">${"Post Bans"}</%block>

<section>
	<h3>IP Bans</h3>
	<table class="zebra v-mid">
		<thead>
			<tr>
				<th>Hash</th>
				<th>Reason</th>
				<th>Added</th>
				<th>Action</th>
			</tr>
			<tr>
				<form action="${request.url}" method="GET">
					<td><input type="text" name="fingerprint" value="${request.GET.get('fingerprint', '')}"></td>
					<td><input type="text" name="reason" value="${request.GET.get('reason', '')}"></td>
					<td></td>
					<td><input type="submit" value="Search"></td>
				</form>
			</tr>
		</thead>
		<tbody>
			% for ban in postbans:
				<tr>
					<td>${ban.fingerprint}</td>
					<td>${ban.reason}</td>
					<td style="white-space: nowrap;">${render_date(ban.added, raw=True, time=False)}</td>
					<form action="${route_path('postban', id=ban.id)}" method="POST">
						<td>
							<input type="hidden" name="_method" value="DELETE" />
							<input type="submit" value="Delete" />
						</td>
					</form>
				</tr>
			% endfor
		</tbody>
	</table>
</section>
