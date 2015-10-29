<?php

function handle() {
  header('Content-Type: text/html');

  chapter('mt', 1);

}

function chapter($book, $chapter) {

print <<<HTML_START
<!DOCTYPE html>
<html>
<head>
  <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
   <style type='text/css'> 

* {font-family: sans-serif}

.verse-nr {color: #ff7d00; font-weight:bold; vertical-align: top}

.parsed {color: grey; font-size:12px;}

   </style>
HTML_START;

print <<<JS

  <script type='text/javascript' src='/inc/line_writer.js'></script>

  <script type="text/javascript">

  var body;
  var text;

  function go_to_strongs(strongs_nr) {
    window.open("https://www.blueletterbible.org/lang/lexicon/lexicon.cfm?strongs=" + strongs_nr + "&t=KJV");
  }

  function main() {

    var canvas = document.getElementById('canvas_griechischer_test');

    tq84.line_writer.init(
       canvas,
      '10cm',
      {left_to_right: true}
    );

    var x = [];
JS;
  
    $dbh = db_connect();
  
    $sth = $dbh -> prepare ('select verse, word_cnt, word_greek, strong_nr_1, strong_nr_2, parsed_1, parsed_2 from bible where book = :book and chapter = :chapter order by word_cnt');
  
    $sth -> execute(array($book, $chapter));

    $last_verse = 0;
  
    while ($row = $sth->fetch()) {

      $elem = '<table border=0 onclick="go_to_strongs(' . $row['strong_nr_1'] . ');">';

      print "// " . $row['verse'] . "\n";

      if ($last_verse != $row['verse']) {

        $last_verse = $row['verse'];

        $elem .= '<tr><td rowspan=3 class="verse-nr">' . $last_verse . '</td>';

      }
      else {
        $elem .= '<tr>';

      }
      $elem .=     '<td>' . $row['word_greek' ]  . '</td></tr>';
      $elem .= '<tr><td class="parsed">' . $row['parsed_1']   . '</td></tr>';
//    $elem .= '<tr><td>' . $row['parsed_2']   . '</td></tr>';
      $elem .= "</table>";

      print "x.push('" . $elem . "');\n";
  
    }

print <<<JS

     var ret = tq84.line_writer.emit(30, x);
     canvas.style.height = ret.height_px + 'px';

  }

  </script>
JS;

  print "</head><body onload='main();'><div id='canvas_griechischer_test'></div></body></html>";
}

function db_connect() {
  $db = new PDO("sqlite:BP05FNL.db"); 
  $db -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  return $db;
}

?>
