<?php
	// Connects to the Database 
	include('connect.php');
	connect();
	
	// include the crypto lib
	include('cryptolib.php');
	
	//if the login form is submitted 
	if (!isset($_GET['pid'])) {
		
		if (isset($_GET['delpid'])){
			mysql_query("DELETE FROM threads WHERE id = '".$_GET[delpid]."'") or die(mysql_error());
		}
			header("Location: members.php");
	}
		?>  
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>hackme</title>
<link href="style.css" rel="stylesheet" type="text/css" media="screen" />
<?php
	include('header.php');
	if(!isset($_COOKIE['hackme'])){
		 die('Why are you not logged in?!');
	}else
	{
		// hackme cookie decryption
		$userName = decryptCookie($_COOKIE['hackme']);
		print("<p>Logged in as <a>$userName</a></p>");

		// fix for 1.2 cookie is updated
		$extra = mysql_query("SELECT extra FROM users WHERE username = '$userName'") or die(mysql_error());

		while($thisextra = mysql_fetch_array( $extra )){
				
			if (!(md5($_COOKIE['hackme']) == $thisextra['extra']))
			{
				die('<p>COOKIE HIJACKING IN PROGRESS!</p>');
			}
		}
	}
?>
<?php
	// p4.2 defense
	// SQL special string skipping
	$userinputtmp = mysql_real_escape_string($_GET[pid]);
	$sqlinput = ["'", ";", ",", "#", "-", "&", "%", "|", "\\", "or ", "and ", "\""];
	$pidinput = str_replace($sqlinput, "", $userinputtmp);

	$threads = mysql_query("SELECT * FROM threads WHERE id = '$pidinput'") or die(mysql_error());
	while($thisthread = mysql_fetch_array( $threads )){
?>
	<div class="post">
	<div class="post-bgtop">
	<div class="post-bgbtm">
		<h2 class="title"><a href="show.php?pid=<?php echo $thisthread[id] ?>"><?php echo $thisthread[title]?></a></h2>
							<p class="meta"><span class="date"> <?php echo date('l, d F, Y',$thisthread[date]) ?> - Posted by <a href="#"><?php echo $thisthread[username] ?> </a></p>
         
         <div class="entry">
			
            <?php echo $thisthread[message] ?>
            					
		 </div>
         
	</div>
	</div>
	</div>
    
    <?php
		$userName = decryptCookie($_COOKIE['hackme']);
		if ($userName == $thisthread[username])
		{
	?>
    	<a href="show.php?delpid=<?php echo $thisthread[id]?>">DELETE</a>
    <?php
		}
	?> 

<?php
}
	include('footer.php');
?>
</body>
</html>

