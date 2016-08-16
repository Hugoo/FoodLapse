<?php
//open up the log file
$file = fopen('/home/pi/prog/html/logX.html', 'a') or die("can't open file"); 

//write the time of access

$time = date('H:i dS F');
fwrite($file, '<b>Time:</b>'.$time.'<br/>' );

//write the users IP address
fwrite( $file, '<b>Ip Address:</b>'.$_SERVER['REMOTE_ADDR'].'<br/>');


//write the users browser details
fwrite( $file, '<b>Browser:</b>'.$_SERVER['HTTP_USER_AGENT'].'<hr/>');

//and finial, close the log file
fclose( $file );
?>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html>
	<head>
		<title>FoodLapse Beta</title>
		<link rel="shortcut icon" type="image/x-icon" href="http://www.gielve.com/img/favicon.ico" />
                <style type="text/css">
                  * { margin: 0; padding: 0; border: 0; }
                  body { background: #F5F5F5; color: #48494A; border-top: 4px solid #868A97; font-family: ‘Metrophobic’, Arial, serif; font-weight: 400;}
                  body a { text-decoration: none; color: #5C9FC0;}
                  body a:hover { text-decoration: underline; }
            
                  #middle { background: #fff; width: 540px; margin: 100px auto; clear: both; padding: 32px 40px; font-weight: 300; font-size: 25px; line-height: 30px; -webkit-box-shadow: 0 1px 2px #ccc; -moz-box-shadow: 0 1px 2px #ccc; box-shadow: 0 1px 2px #ccc; -webkit-border-radius: 8px; -moz-border-radius: 8px; border-radius: 8px; color: #666; }
                  #middle a { color: #AEB7D4; }
                  #middle p { padding-bottom: 14px; }
                 
                  div.footer { margin: 20px auto; clear: both; display: block; width: 880px; letter-spacing:1px; list-style-type: none; border-top: 1px solid #fff; -webkit-box-shadow: 0 -1px 0 #ddd; -moz-box-shadow: 0 -1px 0 #ddd; box-shadow: 0 -1px 0 #ddd; padding: 20px 0; text-align: center; }
                  div.footer  a, div.footer span { margin: 0 auto; font-size: 9px; color:#48494A;}

                  #ctr img {
					    display: block;
					    margin-left: auto;
					    margin-right: auto;
					}
                </style>
	</head>
	<body>
		<div id="middle">
		<div id="ctr"><img src="giphy.gif" height="300px" alt=gif></div>
		<br/>
		<p>Everyday at ~11:59pm, find the daily foodcam timelapse in the <a href="/videos">videos</a> folder.</p>
		<h5>Stats</h5>
		<p><?php
		$fi = new FilesystemIterator("../raw/", FilesystemIterator::SKIP_DOTS);
		$files = scandir('../raw/', SCANDIR_SORT_DESCENDING);
		$numberOfFiles = iterator_count($fi);
		if ($numberOfFiles==0) {$time = "-";} else {$time = date('h:i:s A' ,filectime("../raw/".$files[0]));}
		exec("pgrep python", $pids);
		if(empty($pids)) {
			print("foodcam.py is not running<br/>");
		}
		else {
			printf("foodcam.py is running<br/>");
		}
		printf("Pictures taken today : %d<br/>Last picture taken at : %s", $numberOfFiles, $time); ?></p>
		</div>

		<div id="ctr">
		<a href="how.html"><img src="rpi.png" alt="running on a RPi 3"></a>
		</div>
		<div class="footer">
      <span>hmasclet@media - Page inspired by <a href="http://t.co/">t.co</a></span>
    </div>
		

	</body>
</html>
