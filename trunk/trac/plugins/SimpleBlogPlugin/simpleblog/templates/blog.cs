<?cs include "header.cs"?>

<div id="ctxtnav" class="nav"></div>

<div id="content" class="wikipage">
<?cs
each:event = blog.events ?>
<h1><a href="<?cs var:event.href ?>"><?cs var:event.title ?></a></h1>
<p><?cs var:event.description ?></p>
<p style="font-size: smaller; color: gray; border-top: 1px solid #eee; margin-bottom: 3em;">
<?cs var:event.date ?> | <?cs var:event.author ?> |
<a href="<?cs var:event.href ?>" title="permalink" style="border-bottom-style: none;">#</a><?cs
if:event.comments ?> | <?cs var:event.comments ?> comments<?cs /if ?><?cs
/each ?>

<div id="help">
 <hr />
 <strong>Note:</strong> See <a href="<?cs var:trac.href.wiki ?>/SimpleBlogPlugin">SimpleBlogPlugin</a>
 for information about the blog view.
</div>

</div>

<?cs include "footer.cs"?>
