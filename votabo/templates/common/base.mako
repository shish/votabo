<%!
import webhelpers.util as wu
%>
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
<html>
	<head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title><%block name="title">Untitled Page</%block> - Votabo</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">

        <!-- Place favicon.ico and apple-touch-icon.png in the root directory -->

        <link rel="stylesheet" href="${static_url('css/normalize.css')}">
        <link rel="stylesheet" href="${static_url('css/main.css')}">
        <link rel="stylesheet" href="${static_url('css/menuh.css')}">
		<link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/themes/flick/jquery-ui.css">
		<link rel="stylesheet" href="${static_url('css/jquery.tagit.css')}">
        <link rel="stylesheet/less" href="${static_url('css/votabo.less')}">
        <link rel="stylesheet" href="${static_url('css/shm-uploader.css')}">
        <script src="${static_url('js/vendor/modernizr-2.6.2.min.js')}"></script>
        <script src="${static_url('js/vendor/less-1.3.3.min.js')}"></script>
	</head>
	<body class="<%block name='bodyclass'></%block>">
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->
		<%block name="headerblock">
			<header>
				<!-- <h1><%block name="header"></%block></h1> -->
				<%include file="header.mako" />
			</header>
		</%block>
		<%block name="bodyblock">
			<nav>
				<%block name="nav">
					<section>
						<h3>Navigation</h3>
						<div>
							% if pager:
								% if pager.previous_page:
									<a href="${wu.update_params(request.url, page=pager.previous_page)}">Prev</a> |
								% else:
									Prev |
								% endif
							% endif
							<a href="${route_path('posts')}">Index</a>
							% if pager:
								% if pager.next_page:
									| <a href="${wu.update_params(request.url, page=pager.next_page)}">Next</a>
								% else:
									| Next
								% endif
							% endif

							<%block name="navblock_extra"></%block>
						</div>
					</section>
				</%block>
			</nav>
			<article>
				<section>
					<div style="text-align: center; font-weight: bold; font-size: x-large; color: red;">
						Please be vigilant and report any "underage content" that breaks
						<a href="${route_path('wiki', title='Notes')}">our rules on the matter</a>.
						Read those rules first though, or you may be banned.
					</div>
				</section>

				${self.body()}

				% if pager:
					<section id="paginator">
						${pager.pager("$link_previous ~3~ $link_next")}
					</section>
				% endif
			</article>
		</%block>
		<%block name="footerblock">
			<footer>
				Images &copy; their respective owners
				<a href="http://code.shishnet.org/votabo/">Votabo</a> &copy;
				<a href="http://www.shishnet.org/">Shish</a> 2013
			</footer>
		</%block>

		<div class="js">
			<script src="${static_url('js/vendor/jquery-1.9.0.min.js')}"></script>
			<script src="${static_url('js/vendor/jquery.timeago-1.0.2.js')}"></script>
			<script src="${static_url('js/vendor/jquery.cookie-0.0.0.min.js')}"></script>
			<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/jquery-ui.min.js"></script>
			<script src="${static_url('js/vendor/jquery.tag-it-2.0.min.js')}" type="text/javascript" charset="utf-8"></script>
			<script src="${static_url('js/plugins.js')}"></script>
			<script src="${static_url('js/main.js')}"></script>
			<script src="${static_url('js/shm-zoomer.js')}"></script>
			<script src="${static_url('js/shm-uploader.js')}"></script>
			<%block name="javascript"></%block>
		</div>
	</body>
</html>
