<?php 
	
    if (isset($_POST['submit'])) {
        $email = $_POST['email'];
        $uname = $_POST['uname'];

        $sToken = "Ssqqt0UiA9kOC6q7EbJOTMN4ZBH5LhFudRDXDv5WjqS";
	    $sMessage = "ปุกาศ มีไอหน้าหนอน\n";
		$sMessage .= "Email: ". $email ."\n";
	    $sMessage .= "User Name: " . $uname . "\n";
	    $sMessage .= "สมัครเข้ามา \n";

        
	    $chOne = curl_init(); 
	    curl_setopt( $chOne, CURLOPT_URL, "https://notify-api.line.me/api/notify"); 
	    curl_setopt( $chOne, CURLOPT_SSL_VERIFYHOST, 0); 
	    curl_setopt( $chOne, CURLOPT_SSL_VERIFYPEER, 0); 
	    curl_setopt( $chOne, CURLOPT_POST, 1); 
	    curl_setopt( $chOne, CURLOPT_POSTFIELDS, "message=".$sMessage); 
	    $headers = array( 'Content-type: application/x-www-form-urlencoded', 'Authorization: Bearer '.$sToken.'', );
	    curl_setopt($chOne, CURLOPT_HTTPHEADER, $headers); 
	    curl_setopt( $chOne, CURLOPT_RETURNTRANSFER, 1); 
	    $result = curl_exec( $chOne ); 

	    //Result error 
	    if(curl_error($chOne)) 
	    { 
	    	echo 'error:' . curl_error($chOne); 
	    } 
	    else { 
	    	$result_ = json_decode($result, true); 
	    	echo "status : ".$result_['status']; echo "message : ". $result_['message'];
	    } 
	    curl_close( $chOne );  
        }

?>