<?php include_once "loli-list.php"; ?><!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>Loli Cries!</title>
		<meta name="viewport" content="width=device-width" />
		<link rel="stylesheet" type="text/css" href="style.css" />
		<link rel="icon" type="image/png" href="favicon.png" />
	</head>
	<body>
		<h1><span class="h">❤</span> Loli Cries! <span class="h">❤</span></h1>
		<div id="m">
<?php
	foreach ($lolis as $loli) {
		$phpsux = split(' ', $loli['name']);
		$key = strtolower($phpsux[0]);
		echo "\t\t\t<div class=\"i\" id=\"$key\">\n\t\t\t\t<h2>$loli[name] (<i>$loli[anime]</i>)</h2>\n\t\t\t\t<img src=\"$loli[pic]\" />";
		foreach ($loli['cries'] as $cry)
			echo "\n\t\t\t\t<div class=\"c\">$cry[0]</div> <audio src=\"$cry[1]\" controls=\"controls\"></audio><br />";
		echo "\n\t\t\t</div>\n";
	}
	echo "\t\t\t<div style=\"clear:left;\"></div>\n\t\t</div>\n";
?>
		<footer>
			<p class="csr">Comment/Submit/Request: #/dev/null @ irc.yozora-irc.net</p>
			<p>2010-2011 - The loli ❤ team</p>
		</footer>
	</body>
</html>

