<%inherit file="../common/base.mako" />
<%namespace file="../common/funcs.mako" import="*" />

<%block name="title">${"Alias List"}</%block>
<%block name="header">${"Alias List"}</%block>

<%block name="navblock_extra">
	<br/>&nbsp;
	<br/><a href="${route_path('aliases-csv')}">Download CSV</a>
</%block>

<section>
	<h3>Alias List</h3>
	<table class="zebra">
		<thead>
			<tr>
				<th>From</th>
				<th>To</th>
				<th>Action</th>
			</tr>
			<tr>
				<form action="${request.url}" method="GET">
					<td><input type="text" name="oldtag" value="${request.GET.get('oldtag', '')}" placeholder="Search: from" /></td>
					<td><input type="text" name="newtag" value="${request.GET.get('newtag', '')}" placeholder="Search: to" /></td>
					<td><input type="submit" value="Search" /></td>
				</form>
			</tr>
		</thead>
		<tbody>
			% for alias in aliases:
				<tr>
					<td>${alias.oldtag}</td>
					<td>${alias.newtag}</td>
					<form action="${route_path('alias', id=alias.oldtag)}" method="POST">
						<input type="hidden" name="_method" value="DELETE" />
						<td>
							<input type="submit" value="Delete" />
						</td>
					</form>
				</tr>
			% endfor
		</tbody>
		<tfoot>
			<tr>
				<form action="${route_path('aliases')}" method="POST">
					<td><input type="text" name="oldtag" value="" placeholder="Create: from" /></td>
					<td><input type="text" name="newtag" value="" placeholder="Create: to" /></td>
					<td><input type="submit" value="Create" /></td>
				</form>
			</tr>
		</tfoot>
	</table>
</section>
