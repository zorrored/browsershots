<script type="text/javascript">searchHighlight()</script><?cs
if:len(chrome.links.alternate) ?>
<div id="altlinks"><h3>Download in other formats:</h3><ul><?cs
 each:link = chrome.links.alternate ?><?cs
  set:isfirst = name(link) == 0 ?><?cs
  set:islast = name(link) == len(chrome.links.alternate) - 1?><li<?cs
    if:isfirst || islast ?> class="<?cs
     if:isfirst ?>first<?cs /if ?><?cs
     if:isfirst && islast ?> <?cs /if ?><?cs
     if:islast ?>last<?cs /if ?>"<?cs
    /if ?>><a href="<?cs var:link.href ?>"<?cs if:link.class ?> class="<?cs
    var:link.class ?>"<?cs /if ?>><?cs var:link.title ?></a></li><?cs
 /each ?></ul></div><?cs
/if ?>

<div class="menu lightgray" id="bottom">
<ul class="left"><li class="first"><a
href="/trac/wiki/ContactDetails">Contact</a></li><li><a
href="/trac/wiki/TermsOfUse">Terms of Use</a></li><li><a
href="/trac/wiki/PrivacyPolicy">Privacy Policy</a></li></ul>
<ul class="right"><li class="first"><a
href="http://validator.w3.org/check?uri=referer">XHTML 1.1</a></li><li><a
href="http://jigsaw.w3.org/css-validator/check/referer">CSS</a></li></ul>
<div class="clear"></div>
</div>

</div>
</body>
</html>
