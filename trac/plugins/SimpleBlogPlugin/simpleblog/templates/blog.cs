<?cs include "header.cs"?>

<div id="ctxtnav" class="nav"></div>

<div id="content" class="blog">
<?cs
each:event = blog.events ?>
<h1><a href="<?cs var:event.href ?>"><?cs var:event.title ?></a></h1>
<p><?cs var:event.description ?></p>
<p>Posted <?cs var:event.date ?> by <?cs var:event.author ?><?cs
if:event.comment ?>: <?cs var:event.comment ?><?cs /if ?><?cs
if:event.updated.date ?><br />Updated <?cs var:event.updated.date ?> by <?cs var:event.updated.author ?><?cs /if ?><?cs
if:event.updated.comment ?>: <?cs var:event.updated.comment ?><?cs /if ?><?cs
/each ?>

<div id="help">
 <hr />
 <strong>Note:</strong> See <a href="<?cs var:trac.href.wiki ?>/SimpleBlogPlugin">SimpleBlogPlugin</a>
 for information about the blog view.
</div>

</div>

<?cs include "footer.cs"?>
