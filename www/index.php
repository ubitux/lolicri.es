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

	<header>
	  <hgroup>
	    <h1>Loli Cries!</h1>
	    <h2>The internet loli database</h2>
	  </hgroup>
	</header>

	<section id="lolis">
	  <?php foreach ($lolis as $l) { ?>
	  <article>
	    <header>
	      <hgroup>
	        <h1><?php echo $l['name'] ?></h1>
	        <h2><?php echo $l['anime'] ?></h2>
	      </hgroup>
	    </header>

	    <img src="<?php echo $l['pic']; ?>" />
	    <dl>
	      <?php foreach ($l['cries'] as $cry) {?>
	      <dt><?php echo $cry[0] ?></dt>
	      <dd><audio preload="none" src="<?php echo $cry[1] ?>" controls="controls"></audio></dd>
	      <?php } ?>
	    </dl>
	  </article>
	  <?php } ?>
	</section>

		<footer>
			<p>Comment/Submit/Request: #/dev/null @ irc.yozora-irc.net</p>
			<p class="loli❤">2010-2011 - The loli ❤ team</p>
		</footer>
	</body>
</html>
