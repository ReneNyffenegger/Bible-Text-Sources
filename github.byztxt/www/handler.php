<?php

# include($_SERVER[DOCUMENT_ROOT] . "/../$test_or_prod/php/db.php");

# print ("<b>Hello</b>");
#

start_html();
$db = db_connect('BP5.db');

$uri = $_SERVER['REQUEST_URI'];

# Get uri's last portion:
$uri_ = end(explode('/', $uri));

# print_r(SQLite3::version());

if ($uri_ == 'index') {
  $db = db_connect('BP5.db');
  index($db);
}
elseif ($uri_ == 'Strongs') {
  $db = db_connect('strongs.db');
  strongs_alle($db);
}
elseif (preg_match('/^Kapitel-(\w+)-(\d+)$/', $uri_, $m)) {
  $db = db_connect('BP5.db');
  print_chapter($db, $m[1], $m[2]);
}
elseif (preg_match('/^Strongs-(\d+)$/', $uri_, $m)) {
  $db = db_connect('BP5.db');
  show_verses_with_strongs($db, $m[1]);
}
else {
  print "oh no: $uri!";
}


print "</body></html>";

function db_connect($sqlite_file) { #_{
  $db_file = $_SERVER[DOCUMENT_ROOT] . "/../db/Biblisches/Grundtext/$sqlite_file";

  if (! file_exists($db_file)) {
    echo "DB does not exist!";
    exit(1);
  }
  $db = new PDO("sqlite:$db_file"); 
# $db -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  return $db;
} #_}

# function db_cnt_table($dbh, $table_name) { #_{
#   return db_sel_1_row_1_col($dbh, "select count(*) from $table_name");
# } #_}

function db_prep_exec($dbh, $sql, $params = array()) { #_{

  $sth = $dbh -> prepare ($sql);

  if (!$sth) {
     print ("! preparation failed<br>");
     print_r($dbh->errorInfo());
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

function db_prep_exec_fetchrow($dbh, $sql, $params = array()) { #_{

  $sth = db_prep_exec($dbh, $sql, $params);
  if (! $sth) {
     print ("db_prep_exec failed<br>");
     return 0;
  }

  return $sth -> fetch();

} #_}

function index($db) { #_{

  $res = db_prep_exec_fetchall($db, 'select distinct b.abbr, v.c from book b join verse v on b.abbr = v.b order by b.ord, v.v', array());
  foreach ($res as $row) {
    printf("<a href='Kapitel-%s-%d'>%s-%d</a> ", $row['abbr'], $row['c'], $row['abbr'], $row['c']);
  }

  print "</body></html>";

} #_}

function strongs_alle($db) { #_{

  $res = db_prep_exec_fetchall($db, 'select nr, word from strongs_greek', array());

  if (! $res) {
    print("Well...<br>");
    exit(1);
  }

  print("<table>");
  foreach ($res as $row) {
    printf("<tr><td><a href='Strongs-%d'>%s</a></td></tr>", $row['nr'], $row['word']);
  }
  print("</table>");

} #_}

function show_verses_with_strongs($db, $nr) { #_{

  $db_strongs = db_connect('strongs.db');
  $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word, text_de from strongs_greek where nr = ?', array($nr));

  print("<h1>Strongs $nr (" . $row_strongs['word'] .")</h1>");

  print "Google-Übersetzung vom Strong's-Eintrag:";
  print "<pre style='background-color:#c9faff; border:1px solid black'><code>" . $row_strongs['text_de'] . "</code></pre>";


  $res_1 = db_prep_exec_fetchall($db, 'select distinct v_id, b, c, v from word_v where strongs = ?', array($nr));

  foreach ($res_1 as $row_1) {
    printf("<p><a href='Kapitel-%s-%d'>%s-%d-%d</a>: ", $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v']);

    $res_2 = db_prep_exec_fetchall($db, '
      select
        strongs, txt
      from
        word
      where
        v = ?
      order by
        no
       ', array($row_1['v_id'])
    );
     
     foreach ($res_2 as $row_2) {
       if ($row_2['strongs'] == $nr) {
         print("<b>");
       }
       printf("<a href='Strongs-%d'>%s</a> ", $row_2['strongs'], to_greek_letters($row_2['txt']));
       if ($row_2['strongs'] == $nr) {
         print("</b>");
       }
     }

  }

# $res = db_prep_exec_fetchall($db, "with v as (
#     select distinct b, c, v from word_v where strongs = $nr
#   )
#   select
#     w.strongs, w.b, w.c, w.v, w.word
#   from
#     word_v w join v on w.b = v.b and w.c = v.c and w.v = v.v
#   order by
#     w.b, w.no
#  ", array()
# ); 

# $last_b = '?';
# $last_c = 0;
# $last_v = 0;

# foreach ($res as $row) {
#   if ($last_b != $res['b'] or $last_c != $res['c'] or $last_v != $res['v']) {

#     printf("<p><a href='%s-%d'>%s-%d-%d</a>: ", $res['b'], $res['c'], $res['b'], $res['c'], $res['v']);

#     $last_b = $res['b'];
#     $last_c = $res['c'];
#     $last_v = $res['v'];
#   }

#   printf("<a href='Strongs-%d'>%s</a> ", $res['strongs'], to_greek_letters($res['word']));
# }

} #_}

function print_chapter($db, $abbr, $c) { #_{

  $res = db_prep_exec_fetchall($db, 'select strongs, v, word, parsed from word_v where b=? and c=? order by no', array($abbr, $c));

  if (! $res) {
    print("hmm, what now?<br>");
    exit(1);
  }

  print "<table border=1>";
  foreach ($res as $row) {
    printf ("<tr><td>%d</td><td><a href='Strongs-%d'>%s</a></td><td>%s</td></tr>",  $row['v'], $row['strongs'], to_greek_letters($row['word']), $row['parsed']);
  }
  print "</table>";

  print "<p><a href='index'>Inhaltsverzeichnis</a>";
} #_}

function strtr_utf8($str, $from, $to) { #_{
    $keys = array();
    $values = array();
    preg_match_all('/./u', $from, $keys);
    preg_match_all('/./u', $to, $values);
    $mapping = array_combine($keys[0], $values[0]);
    return strtr($str, $mapping);
} #_}

function to_greek_letters($letters) { #_{
   return strtr_utf8($letters, 'abcdefghiklmnopqrstuvwxyz', 'αβχδεφγηικλμνοπψρστυςωξθζ');
} #_}

function start_html() { #_{
 print "<!DOCTYPE html>
<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
<! -- meta name='description' content='' / -->
<title>$title</title>
<style>


</style>
";

} #_}

?>
