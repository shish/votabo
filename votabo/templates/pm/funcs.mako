<%!
from votabo.models import PrivateMessage
%>

<%namespace file="../common/funcs.mako" import="*" />

<%def name="render_pm_list(duser, onlyUnread=False)">
	<section>
		<h3>${"Unread " if onlyUnread else ' '}Private Messages</h3>
		<table class="zebra sortable">
			<tr>
				<th>R?</th>
				<th>Subject</th>
				<th>From</th>
				<th style="width: 10em;">Date</th>
				<th>Action</th>
			</tr>
			<%
			if onlyUnread:
				pmList = [pm for pm in duser.pm_inbox if not pm.is_read]
			else:
				pmList = duser.pm_inbox
			%>
			% if pmList:
				% for pm in pmList:
					<tr>
						<td>${"Y" if pm.is_read else "N"}</td>
						<td><a href="${route_path('pm', id=pm.id)}">${pm.subject or "(No Subject)"}</a></td>
						<td><a href="${route_path('user', name=pm.user_from.username)}">${pm.user_from.username}</a></td>
						<td>${render_date(pm.sent_date, raw=True)}</td>
						<form action="${route_path('pm', id=pm.id)}" method="POST">
							<td>
								<input type="hidden" name="_method" value="DELETE" />
								<input type="submit" value="Delete" />
							</td>
						</form>
					</tr>
				% endfor
			% else:
				<tr>
					<td colspan="5">No Messages</td>
				</tr>
			% endif
			<tr>
				<td colspan="5"><a href="${route_path('pms')}">View All</a></td>
			</tr>
		</table>
	</section>
</%def>

<%def name="render_pm_composer(to, subject='')">
	<section>
		<h3>Write a PM to ${to.username}</h3>
		<div class="blockbody">
			<form method="POST" action="${route_path('pms')}">
				<input type="hidden" name="to" value="${to.username}">
				<table class="form" style="width: 400px; margin: auto;">
					<tr>
						<td>Subject:</td>
						<td><input type="text" name="subject" value="${subject}"></td>
					</tr>
					<tr>
						<td colspan="2">
							<textarea name="content" rows="5"></textarea>
						</td>
					</tr>
					<tr>
						<td colspan="2">
							<input type="submit" value="Send" />
						</td>
					</tr>
				</table>
			</form>
		</div>
	</section>
</%def>
