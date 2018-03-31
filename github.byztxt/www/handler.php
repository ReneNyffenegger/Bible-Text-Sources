<?php

# include($_SERVER[DOCUMENT_ROOT] . "/../$test_or_prod/php/db.php");

# print ("<b>Hello</b>");
#

start_html();
$db = db_connect();

if (! $db) {
  print "<br>Could not connect to DB";
  exit(1);
}
$uri = $_SERVER['REQUEST_URI'];

# Get uri's last portion:
$uri_ = end(explode('/', $uri));

# if (preg_match('/([^\/]+)$/', $uri, $m)) {
#   $uri_ = $m[1];
# }
# else {
#   print "hmm?";
# }

if (preg_match('/^Kapitel-(\w+)-(\d+)$/', $uri_, $m)) {
  print_chapter($db, $m[1], $m[2]);
}
else {
  print "oh no!";
}

# print "db = $db";

print "</body></html>";

function db_connect() {
  $db_file = $_SERVER[DOCUMENT_ROOT] . '/../db/Biblisches/Grundtext/BP5.db';
  if (! file_exists($db_file)) {
    echo "DB does not exist!";
    return 0;
  }
  $db = new PDO("sqlite:$db_file"); 
# $db -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  return $db;
}


# function db_cnt_table($dbh, $table_name) { #_{
#   return db_sel_1_row_1_col($dbh, "select count(*) from $table_name");
# } #_}

function db_prep_exec($dbh, $sql, $params = array()) { #_{

  $sth = $dbh -> prepare ($sql);

  if (!$sth) {
     print ("! preparation failed<br>");
     return 0;
  }

  $sth -> execute($params);

  return $sth;

} #_}

function db_prep_exec_fetchall($dbh, $sql, $params = array()) { #_{

  $sth = db_prep_exec($dbh, $sql, $params);
  if (! $sth) {
     print ("db_prep_exec failed<br>");
     return 0;
  }

  return $sth -> fetchAll();

} #_}


function print_chapter($db, $abbr, $c) {

  $res = db_prep_exec_fetchall($db, 'select strongs, v, word, parsed from word_v where b=? and c=? order by no', array($abbr, $c));

  if (! $res) {
    print("hmm, what now?<br>");
    exit(1);
  }
# 
  print "<table border=1>";
  foreach ($res as $row) {
    printf ("<tr><td>%d</td><td>%d</td><td>%s</td><td>%s</td></tr>", $row['strongs'], $row['v'], to_greek_letters($row['word']), $row['parsed']);
  }
  print "</table>";
}


function strtr_utf8($str, $from, $to) {
    $keys = array();
    $values = array();
    preg_match_all('/./u', $from, $keys);
    preg_match_all('/./u', $to, $values);
    $mapping = array_combine($keys[0], $values[0]);
    return strtr($str, $mapping);
}


function to_greek_letters($letters) {
   return strtr_utf8($letters, 'abcdefghiklmnopqrstuvwxyz', 'αβχδεφγηικλμνοπψρστυςωξθζ');
}

function start_html() {
 print "<!DOCTYPE html>
<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
<! -- meta name='description' content='' / -->
<title>$title</title>
<style>


</style>
";
 
}

?>

