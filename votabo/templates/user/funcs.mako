<%def name="user_block_small()">
	% if request.user.category != "anonymous":
		<section>
			<h3>Logged in as ${request.user.username}</h3>
			<div>
				<a href="${route_path('user', name=request.user.username)}">My Profile</a> |
				<a href="${route_path('aliases')}">Aliases</a> |
				<a href="${route_path('ipbans')}">IP Bans</a> |
				<a href="${route_path('postbans')}">Post Bans</a> |
				<a href="${route_path('users')}">User List</a> |
				<a href="${route_path('pms')}">Private Messages</a> |
				<a href="${route_path('logs')}">Event Log</a> |
				<!--
				<a href="/setup">Board Config</a> |
				<a href="/admin">Board Admin</a> |
				-->
				<a href="${route_path('session-delete')}">Log Out</a>
			</div>
		</section>
	% else:
		<section>
			<h3>Log In</h3>
			<div>
				<form action="${route_path('session')}" method="POST">
					<table class="form" style="width: 100%;">
						<tr>
							<th>Username</th>
							<td><input type="text" name="username"></td>
						</tr>
						<tr>
							<th>Password</th>
							<td><input type="password" name="password"></td>
						</tr>
						<tr>
							<td colspan="2"><input type="submit" value="Log in"></td>
						</tr>
					</table>
				</form>
			</div>
		</section>
	% endif
</%def>
