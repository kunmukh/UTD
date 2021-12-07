<?php
	
	// Connects to the Database 
	include('connect.php');
	connect();

	include('cryptolib.php');
	
	//if the login form is submitted 
	if (isset($_POST['submit'])) {
		
		$_POST['username'] = trim($_POST['username']);
		if(!$_POST['username'] | !$_POST['password']) {
			die('<p>You did not fill in a required field.
			Please go back and try again!</p>');
		}

		// p4.2 defense
		// SQL special string skipping
		$userinputtmp = mysql_real_escape_string($_POST['username']);
		$sqlinput = ["'", ";", ",", "#", "-", "&", "%", "|", "\\", "or ", "and ", "\""];
		$userinput = str_replace($sqlinput, "", $userinputtmp);

		$check = mysql_query("SELECT * FROM users WHERE username = '$userinput'")or die(mysql_error());
		
		// fix1 and 2: password check as well as checking the salted password
		$pass = mysql_query("SELECT pass FROM users WHERE username = '$userinput'")or die(mysql_error());

		while($thispass = mysql_fetch_array( $pass )){
			if (!(password_verify($_POST['password'], $thispass['pass'])))
			{
				die('<p>Password DID NOT MATCH.
				Please go back and try again!</p>');
			}
		}

		//Gives error if user already exist
 		$check2 = mysql_num_rows($check);
		if ($check2 == 0) {
			die("<p>Sorry, user name does not exisits.</p>");
		}
		else
		{
			$hour = time() + 3600;

			$val = encryptCookie($_POST['username']);
			// fix 1.2.3
			// hackme cookie is encrypted
			// fix 2.2 httponly flag set to true
			setcookie(hackme, $val, $hour, null, null, null, true);

			// fix 1.2 session, add the session key in extra
			$hash64 = md5($val);
			mysql_query("UPDATE users SET extra='".$hash64."' WHERE username = '".$_POST['username']."'") or die(mysql_error());

			// fix 1.2.1
			// cookie['hackme_pass'] removed 
			header("Location: members.php");			
		}
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
				$userName = decryptCookie($_COOKIE['hackme']);

				// fix 1.2: if username not in the db kill
				$user = mysql_query("SELECT username FROM users")or die(mysql_error());

				$userarr = array();
				
				while(($u = mysql_fetch_array( $user ))){
					$userarr[] = $u['username'];
				}				

				if (!(in_array($userName, $userarr))){				
					die('Username does NOT exists!!!');
				}
				
				// fix for 1.2 cookie is updated
				$userName = decryptCookie($_COOKIE['hackme']);

				$extra = mysql_query("SELECT extra FROM users WHERE username = '".$userName."'") or die(mysql_error());

				while($thisextra = mysql_fetch_array( $extra )){
				
					if (!(md5($_COOKIE['hackme']) == $thisextra['extra']))
					{
						die('<p>COOKIE HIJACKING IN PROGRESS!</p>');
					}
				}				
				print("<p>Logged in as <a>$userName</a></p>");
			}
			?>
        </div>
    </div>
</div>

<?php
	$threads = mysql_query("SELECT * FROM threads ORDER BY date DESC")or die(mysql_error());
	while($thisthread = mysql_fetch_array( $threads )){
?>
	<div class="post">
	<div class="post-bgtop">
	<div class="post-bgbtm">
		<h2 class="title"><a href="show.php?pid=<?php echo $thisthread['id'] ?>"><?php echo $thisthread['title']?></a></h2>
							<p class="meta"><span class="date"> <?php echo date('l, d F, Y',$thisthread[date]) ?> - Posted by <a href="#"><?php echo $thisthread[username] ?> </a></p>

	</div>
	</div>
	</div> 

<?php
}
	include('footer.php');
?>
</body>
</html>

