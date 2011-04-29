<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="/media/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
	<link rel="stylesheet" href="/media/css/taf-kickoff-m.css" type="text/css" media="screen" title="no title" charset="utf-8">
	<link rel="stylesheet" href="/media/css/main.css" type="text/css" media="screen" title="no title" charset="utf-8">
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
	<div id="header">
		<h1><a href="/"><span class="beta">&beta;</span>bj&ouml;rnssaga</a></h1>
	</div>
	<div id="content">
		<?php
		if ($_GET['draft'] && $_GET['slug']) {
			$filename = 'draft_' . $_GET['slug'] . '.php';
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
	<div id="sidebar">
		
	</div>
</body>
</html>
