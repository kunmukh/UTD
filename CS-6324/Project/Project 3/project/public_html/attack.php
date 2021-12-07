<html>
<body>

<?php
echo $_POST["title"]; 
$content = $_POST["title"]; 
$file = "/home/kxm180046/public_html/vic.txt"; 
$Saved_File = fopen($file, 'a'); 
fwrite($Saved_File, $content); 
fwrite($Saved_File, "\n");
fclose($Saved_File); 
?>

</body>
</html>
