
function showpom( id )
{
	$(id).show();
	var o = 'link' + id;	
	$(o).update('maven pom: <a href="#no_follow" onclick="hidepom(\''+ id +'\');">hide</a>');
}

function hidepom( id )
{
	$( id ).hide();
	var o = 'link' + id;
	$( o ).update('maven pom: <a href="#no_follow" onclick="showpom(\''+ id +'\');">view</a>');
}