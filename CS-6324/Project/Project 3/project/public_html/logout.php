<?php
include('connect.php');
connect();
include('cryptolib.php');

$userName = decryptCookie($_COOKIE['hackme']);

setcookie(hackme, "", time() - 3600);
// fix 1.2 session, remove the session key in extra
mysql_query("UPDATE users SET extra='' WHERE username = '$userName'") or die(mysql_error());

// fix 1.2.1
// cookie['hackme_pass'] removed 
header("Location: index.php");
?>

