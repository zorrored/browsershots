<?cs include "header.cs"?>

<div id="ctxtnav" class="nav"></div>

<div id="content" class="blog">
<?cs
each:event = blog.events ?>
<h2><a href="<?cs var:event.href ?>"><?cs var:event.title ?></a></h2><?cs
  if:event.description ?><p><?cs
   var:event.description ?></p><?cs
  /if ?><?cs
  if:event.date ?><p><?cs
   var:event.date ?></p><?cs
  /if ?><?cs
/each ?>

<div id="help">
 <hr />
 <strong>Note:</strong> See <a href="<?cs var:trac.href.wiki ?>/SimpleBlogPlugin">SimpleBlogPlugin</a>
 for information about the blog view.
</div>

</div>

<?cs include "footer.cs"?>
