<!DOCTYPE html>
<html lang="en">
<head>
	<link rel="stylesheet" href="/media/css/bootstrap.css" rel="stylesheet">
	<link rel="stylesheet" href="/media/css/bootstrap-responsive.css" rel="stylesheet">
	<link rel="stylesheet" href="/media/css/main.css" rel="stylesheet">
	<title>bj&ouml;rnssaga</title>
	<link rel="alternate" type="application/rss+xml" title="RSS"
	      href="http://bjornssaga.com/feed.rss">
	<script type="text/javascript">

	  var _gaq = _gaq || [];
	  _gaq.push(['_setAccount', 'UA-23024996-1']);
	  _gaq.push(['_trackPageview']);

	  (function() {
	    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
	  })();

	</script>
</head>
<body>
	<div id="main" class='row'>
		<div id="content" class='offset2 span6'>
			<?php
			if ($_GET['draft'] && $_GET['slug']) {
				$filename = 'drafts/' . $_GET['slug'] . '.php';
				if (file_exists($filename)){
					include($filename);
				}
				else {
					include('404.php');
				}
			}
			elseif ($_GET['year'] && $_GET['month'] && $_GET['day'] && $_GET['slug']) {
				$filename = $_GET['year'] . $_GET['month'] . $_GET['day'] . '_' . $_GET['slug'] . '.php';
				if (file_exists($filename)){
					include($filename);
				}
				else {
					include('404.php');
				}
			}
			elseif ($_GET['year'] && $_GET['month']) {
				$filename = $_GET['year'] . $_GET['month'] . '.php';
				if (file_exists($filename)){
					include($filename);
				}
				else {
					include('404.php');
				}
			}
			else {
				include('main.php');
			}
			?>
		</div>
		<div id="sidebar" class="sidebar span2">
			<h2><a href="/"><span>b</span>j&ouml;rnssaga</a></h2>
			<h3>Me</h3>
			<p>Independent web developer with a degree in language technology. I like Apple products and complex beers.</p>
			<h3>This</h3>
			<p>An artisanal baked blog. Source is <a href='http://github.com/bjornkri/nagisting'>publicly available</a>, and mostly unreadable.</p>
			<h3>Context</h3>
			<p>I was born in <a href='http://en.wikipedia.org/wiki/Akureyri'>Akureyri</a>, married an <a href='http://en.wikipedia.org/wiki/Orvieto'>Orvietana</a> and we live with our daughter in <a href='http://en.wikipedia.org/wiki/Ghent'>Ghent</a>.</p>
		</div>
	</div>
	<div id="footer" class="row">
		<div class="offset2 span8">
			<p><a rel="license" href="http://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a><br />All original content is licensed under the <a rel="license" href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0 Unported License</a>. except that which is quoted from elsewhere or attributed to others. In short, you may reproduce, reblog, and modify my content, but you must provide proper attribution.</p>
			<p>brewed by <a href="http://github.com/bjornkri/nagisting">nagisting</a>. Built with <a href="http://twitter.github.com/bootstrap/">Bootstrap</a></p>
		</div>
	</div>
	<script src='/media/js/bootstrap.js'></script>
</body>
</html>
