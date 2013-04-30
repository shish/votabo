<%!
import locale
%>
<%inherit file="common/base.mako" />

<%block name="bodyclass">front-page</%block>
<%block name="fullbody">
	<h1><a style='text-decoration: none;' href="${route_path('posts')}"><span>${site_title}</span></a></h1>

	<div class='space' id='links'>
		<a class="shm-clink" data-clink-sel="" href="${route_path('posts')}">Posts</a>
		<a class="shm-clink" data-clink-sel="" href="${route_path('comments')}">Comments</a>
		<a class="shm-clink" data-clink-sel="" href="${route_path('tags')}">Tags</a>
		<a class="shm-clink" data-clink-sel="" href="${route_path('wikis')}">Wiki</a>
	</div>

	<div class='space' id='search'>
		<form action="${route_path('posts')}" method='GET'>
			<table style="width: 500px; margin: auto;"><tr><td width="400">
				<input type="text" class="shm-ac-tags" name="q" placeholder="Enter Keywords" size="36" value="${request.GET.get('q', '')}" />
			</td><td width="50">
				<input type='submit' value='Search' />
			</td></tr></table>
		</form>
	</div>

	<div class='space' id='counter'>
	% for digit in str(post_count):
		<img alt='${digit}' src='${static_path('img/home/counters_1/'+digit+'.gif')}' />
	% endfor
	</div>

	<div class='space' id='foot'>
		<small><small>
			<br><a href='mailto:mailto:staff@paheal.net'>Contact</a> &ndash;
			Serving ${locale.format("%d", post_count, grouping=True)} posts &ndash;
			Running <a href='http://code.shishnet.org/votabo/'>Votabo</a>
		</small></small>
	</div>
</%block>
