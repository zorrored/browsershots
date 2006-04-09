<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head><?cs
 if:project.name_encoded ?>
 <title><?cs if:title ?><?cs var:title ?> - <?cs /if ?><?cs
   var:project.name_encoded ?> - Trac</title><?cs
 else ?>
 <title>Trac: <?cs var:title ?></title><?cs
 /if ?><?cs
 if:html.norobots ?>
 <meta name="ROBOTS" content="NOINDEX, NOFOLLOW" /><?cs
 /if ?><?cs
 each:rel = chrome.links ?><?cs
  each:link = rel ?><link rel="<?cs
   var:name(rel) ?>" href="<?cs var:link.href ?>"<?cs
   if:link.title ?> title="<?cs var:link.title ?>"<?cs /if ?><?cs
   if:link.type ?> type="<?cs var:link.type ?>"<?cs /if ?> /><?cs
  /each ?><?cs
 /each ?><style type="text/css"><?cs include:"site_css.cs" ?></style>
 <script type="text/javascript" src="<?cs
   var:htdocs_location ?>js/trac.js"></script>
<link href="/style/style.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div id="main">

<div class="menu" id="metamenu">
<ul class="left"><li class="first"><a
href="/">Home</a></li><li><a
href="/blog/">Blog</a></li><li><a
href="/trac/wiki/">Wiki</a></li><li><a
href="/trac/timeline/">Timeline</a></li><li><a
href="/trac/roadmap/">Roadmap</a></li><li><a
href="/trac/browser/">Source</a></li><li><a
href="/trac/report/">Tickets</a></li><li><a
href="/trac/wiki/HelpIndex">Help</a></li></ul>
<form action="">
<div class="right">
<select id="langsel">
<option value="en">English</option>
</select>
</div>
</form>
<div class="clear"></div>
</div>

<div class="menu lightgray" id="topmenu">
<ul class="left"><li class="first"><a
href="/screenshots/">Screenshots</a></li><li><a
href="/queue/">Queue</a></li><li><a
href="/factories/">Factories</a></li><li><a
href="/search/">Search</a></li></ul>
<ul class="right"><li class="first"><a
href="/trac/login">Login</a></li><li><a
href="/trac/settings">Settings</a></li></ul>
<p class="right mockup"><a href="http://browsershots.org/blog/2006/03/15/mock-up-for-browsershots-0-3/">Mock-up!</a></p>
<div class="clear"></div>
</div>
