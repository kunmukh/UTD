<?php

function hashCookie($value){
    if(!$value){return false;}

    $text = $value;
    $ciphertext = hash_hmac('md5', $text, 'GFG_DATA');

    return trim($ciphertext); //encode for cookie
}

function encryptCookie($value){
    if(!$value){return false;}
    $cipher = "AES-128-CBC";
    $key = "this is a key";

    // fix 1.2.2
	// nonce added so that cookie is different everytime 
    $ivlen = openssl_cipher_iv_length($cipher="AES-128-CBC");
    $iv = openssl_random_pseudo_bytes($ivlen);
    $ciphertext_raw = openssl_encrypt($value, $cipher, $key, $options=OPENSSL_RAW_DATA, $iv);
    $hmac = hash_hmac('sha256', $ciphertext_raw, $key, $as_binary=true);
    $ciphertext = base64_encode( $iv.$hmac.$ciphertext_raw );

    return trim($ciphertext); //encode for cookie
}

function decryptCookie($value){
    if(!$value){return false;}
    $cipher = "AES-128-CBC";
    $key = "this is a key";

    $c = base64_decode($value);

    $ivlen = openssl_cipher_iv_length($cipher="AES-128-CBC");
    $iv = substr($c, 0, $ivlen);
    $hmac = substr($c, $ivlen, $sha2len=32);
    $ciphertext_raw = substr($c, $ivlen+$sha2len);
    $original_plaintext = openssl_decrypt($ciphertext_raw, $cipher, $key, $options=OPENSSL_RAW_DATA, $iv);

    $calcmac = hash_hmac('sha256', $ciphertext_raw, $key, $as_binary=true);
    if (hash_equals($hmac, $calcmac))
    {
        return trim($original_plaintext);
    }
    else
    {
        return trim($original_plaintext);;
    }
}

?>
