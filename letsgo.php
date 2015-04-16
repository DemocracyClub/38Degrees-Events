<?php

$logFileDone = __DIR__ . DIRECTORY_SEPARATOR . "eventsDone.log";
$logFilePassing = __DIR__ . DIRECTORY_SEPARATOR . "eventsPass.log";

########## Raw Data

$dataObj = json_decode(file_get_contents(__DIR__.DIRECTORY_SEPARATOR."all_data.json"));


########## Log file

$idsDone = array();
foreach(file($logFileDone) as $line) {
	if (trim($line)) {
		$idsDone[] = intval($line);
	}
}

########## Passing file

$idsPassed = array();
foreach(file($logFilePassing) as $line) {
	if (trim($line)) {
		$idsPassed[] = intval($line);
	}
}

$now = new \DateTime("",new \DateTimeZone("UTC"));

foreach($dataObj as $hustingJSON) {

	$urlbits = explode("/", $hustingJSON->link);
	$id = $urlbits[2];

	print "ID " . $id . "\n";

	$start = new \DateTime($hustingJSON->date, new \DateTimeZone("Europe/London"));

	if ($start->getTimestamp() < $now->getTimestamp()) {

		print  "  in the past\n";

	} else if (in_array($id, $idsDone)) {

		print "  already done\n";

	} else if (in_array($id, $idsPassed)) {

		print "  already passed\n";

	} else {

		print "id: ". $id . "\n";
		print "date: ". $hustingJSON->date . "\n";
		print "title: ". $hustingJSON->title . "\n";
		print "description: ". $hustingJSON->description . "\n";
		print "link: https://election.38degrees.org.uk". $hustingJSON->link . "\n";
		print "location_text: ". $hustingJSON->location_text . "\n";

		print "Action? (P)ass/(C)reate/(L)eave \n";



		$result = false;
		do {
			$result = false;
			$line = fgetc(STDIN);
			if (strtolower(substr(trim($line), 0, 1)) == "p") {
				file_put_contents($logFilePassing, "\n".$id."\n", FILE_APPEND);
				$result = true;
			} else if (strtolower(substr(trim($line), 0, 1)) == "c") {

				// TODO!

				file_put_contents($logFileDone, "\n".$id."\n", FILE_APPEND);
				$result = true;
			} else if (strtolower(substr(trim($line), 0, 1)) == "l") {
				$result = true;
			}
		} while (!$result);

	}

}



