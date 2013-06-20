<%namespace file="../post/funcs.mako" import="*" />
<%namespace file="../user/funcs.mako" import="*" />

<table width="100%"><tr><td>
	<a href="${route_path('home')}"><img alt="logo" src="${static_link('img/rule34_logo_top.png')}"></a>
	<div class="flags">
		<a href="${route_path('wiki', title='faqeng')}"><img alt="flag" src="${static_link('img/flags/english-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqger')}"><img alt="flag" src="${static_link('img/flags/german-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqit')}"><img alt="flag" src="${static_link('img/flags/italian-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqnl')}"><img alt="flag" src="${static_link('img/flags/dutch-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqport')}"><img alt="flag" src="${static_link('img/flags/port-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqesp')}"><img alt="flag" src="${static_link('img/flags/spain-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqnor')}"><img alt="flag" src="${static_link('img/flags/norway-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqswe')}"><img alt="flag" src="${static_link('img/flags/swedish-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqfin')}"><img alt="flag" src="${static_link('img/flags/finnish-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqru')}"><img alt="flag" src="${static_link('img/flags/russian-flag.png')}"></a>
		<a href="${route_path('wiki', title='faqchi')}"><img alt="flag" src="${static_link('img/flags/china-flag.png')}"></a>
	</div>
	<form class="header-search" action="${route_path('posts')}" method="GET">
		<table class="search"><tr><td width="80%">
			<input type="text" class="shm-ac-tags" name="q" placeholder="Enter Keywords" size="36" value="${request.GET.get('q', '')}">
		</td><td>
			<input type="submit" value="Search">
		</td></tr></table>
	</form>
	<div id="menuh-container">
	<div id="menuh">

		<ul>
			<li><a href="${route_path('posts')}" class="top_parent">Main</a>
			<ul>
				<li><a href="${route_path('posts')}" class="sub_option">Home page</a></li>
				<li><a href="${route_path('comments')}" class="sub_option">Comments</a></li>
				<li><a href="${route_path('tags')}" class="sub_option">Tags</a></li>
				<li><a href="${route_path('posts/upload')}" class="sub_option">Upload</a></li>
				<li><a href="${route_path('wiki', title='rules')}" class="sub_option">Site rules</a></li>
				<li><a href="${route_path('wiki', title='faq')}" class="sub_option">F.A.Q.</a></li>
				<li><a href="${route_path('wiki', title='staff')}" class="sub_option">Staff</a></li>
				<li><a href="#" class="parent">Contact</a>
				<ul>
					<li><a href="mailto:staff@paheal.net" class="sub_option">Staff</a></li>
					<li><a href="mailto:wiiaboo@paheal.net" class="sub_option">Founder</a></li>
					<li><a href="mailto:webmaster@shishnet.org" class="sub_option">Programmer</a></li>
				</ul>
				</li>
			</ul>
			</li>
		</ul>
		
		<ul>	
			<li><a href="#" class="top_parent">Sites</a>
			<ul>
				<li><a href="http://rule34.paheal.net/" class="sub_option">Rule #34</a></li>
				<li><a href="http://rule63.paheal.net/" class="sub_option">Rule #63</a></li>
				<li><a href="http://cosplay.paheal.net/" class="sub_option">Cosplay</a></li>
				<li><a href="http://rule34c.paheal.net/" class="sub_option">Rule #34c</a></li>
				<!--<li><a href="http://rule35.paheal.net/" class="sub_option">Rule #35</a></li>-->
			</ul>
			</li>
		</ul>
		
		<ul>
			<li><a href="#" class="top_parent">Community</a>
			<ul>
				<!--<li><a href="http://forum.paheal.net" class="sub_option">Forum</a></li>-->
				<li><a href="${route_path('wiki', title='friends')}" class="parent">Friends of paheal</a>
				<li><a href="${route_path('wiki', title='DNP')}" class="parent">DNP List</a>
				<li><a href="#" class="parent">Chat</a>
				<ul>
					<li><a href="irc://irc.rizon.net/rule34" class="sub_option">irc.rizon.net/rule34</a></li>
					<li><a href="http://rule34.paheal.net/themes/rule34/irc/index.html" target="new" class="sub_option">Web Chat</a></li>
				</ul>
				</li>
			</ul>
			</li>
		</ul>
		
		<ul>
			<li><a class="menu top_parent" href="${route_path('wiki', title='Notes')}">ANNOUNCEMENTS</a></li>
		</ul>
		
	</div>
	</div>
</td>

<td style="width: 250px; font-size: 0.85em; padding: 8px;">
	${upload_block_small()}
</td>

<td style="width: 250px; font-size: 0.85em; padding: 8px;">
	${user_block_small()}
</td>


</td></tr></table>
