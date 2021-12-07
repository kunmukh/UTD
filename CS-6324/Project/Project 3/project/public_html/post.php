<?php
// Connects to the Database 
	include('connect.php');
	connect();

	include('cryptolib.php');
	
	//if the login form is submitted 
	if (isset($_POST['post_submit'])) {
		
		$_POST['title'] = trim($_POST['title']);
		if(!$_POST['title'] | !$_POST['message']) {
			include('header.php');
			die('<p>You did not fill in a required field.
			Please go back and try again!</p>');
		}
		
		$userName = decryptCookie($_COOKIE['hackme']);
		// defense for XSS
		// remove form, iframe and script tag
		$messageSanitized = preg_replace('#<script(.*?)>(.*?)</script>#is', '', $_POST[message]);
		$messageSanitized = preg_replace('#<form(.*?)>(.*?)</form>#is', '', $messageSanitized);
		$messageSanitized = preg_replace('#<iframe(.*?)>(.*?)</iframe>#is', '', $messageSanitized);

		mysql_query("INSERT INTO threads (username, title, message, date) VALUES('".$userName."', '". $_POST['title']."', '".$messageSanitized."', '".time()."')")or die(mysql_error());		
		
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
?>
<div class="post">
	<div class="post-bgtop">
		<div class="post-bgbtm">
        <h2 class = "title">hackme bulletin board</h2>
        	<?php
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
            
            <h2 class="title">NEW POST</h2>
            <p class="meta">by <a href="#"><?php echo decryptCookie($_COOKIE['hackme']) ?> </a></p>
            <p> do not leave any fields blank... </p>
            
            <form method="post" action="post.php">
            Title: <input type="text" name="title" maxlength="50"/>
            <br />
            <br />
            Posting:
            <br />
            <br />
            <textarea name="message" cols="120" rows="10" id="message"></textarea>
            <br />
            <br />
            <input name="post_submit" type="submit" id="post_submit" value="POST" />
            </form>
        </div>
    </div>
</div>

<?php
	include('footer.php');
?>
</body>
</html>

