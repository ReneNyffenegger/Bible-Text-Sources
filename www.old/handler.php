<?php


function handle() {
  header('Content-Type: text/html');

  $base = urldecode($_SERVER['REQUEST_URI'] );


  if ($base == '/Biblisches/Grundtext/') {

    index();

    return;
  }

  if (preg_match(  '/([^-]+)-(\d+)/', $_GET['v'], $matched) ) {
    chapter($matched[1], $matched[2]);
    return;
  }

  print "404. " . link_kapitel_auswahl();

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

#canvas_griechischer_text {
  background-color:#f3f3f0;
  position: absolute;
  top: 3cm;
  left:3cm;
  width: 500px;
}

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

    var canvas = document.getElementById('canvas_griechischer_text');

    tq84.line_writer.init(
       canvas,
      '500px',
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

  print "</head><body onload='main();'><div id='canvas_griechischer_text'></div>";

  print link_kapitel_auswahl();

  print "</body></html>";
}

function index() {

  $dbh = db_connect();

print <<<HTML_START
<!DOCTYPE html>
<html>
<head>
  <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
   <style type='text/css'> 

* {font-family: sans-serif}

  </style>
</head>
<body>
HTML_START;


  $res = $dbh->query('select distinct book, chapter from bible order by book, chapter');


  $cur_book = '?';
  foreach ($res as $row) {

    if ($row['book'] != $cur_book) {

      if ($cur_book != '?') {
        print "<br>";
      }

      print "<b>" . $row['book'] . "</b>: ";
      $cur_book = $row['book'];

    }

    print "<a href='?v=" . $row['book'] . '-' . $row['chapter'] . "'>" . $row['chapter'] . "</a> \n";

  }


  print "</body></html>";


}

function link_kapitel_auswahl() {
  return "<a href='/Biblisches/Grundtext/'>Kapitelauswahl</a>";
}

function db_connect() {
  $db = new PDO("sqlite:BP05FNL.db"); 
  $db -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  return $db;
}

?>
