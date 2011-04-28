<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="/media/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
	<link rel="stylesheet" href="/media/css/taf-kickoff-m.css" type="text/css" media="screen" title="no title" charset="utf-8">
	<link rel="stylesheet" href="/media/css/main.css" type="text/css" media="screen" title="no title" charset="utf-8">
	<title>Bj&ouml;rn's saga</title>
</head>
<body>
	<div id="header">
		<h1><a href="/">Bj&ouml;rn's saga</a></h1>
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
