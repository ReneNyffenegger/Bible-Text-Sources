<?php


# $db = db_connect('BP5.db');

$uri = $_SERVER['REQUEST_URI'];

# Get uri's last portion:
$uri_ = end(explode('/', $uri));

# print_r(SQLite3::version());

if ($uri_ == 'index') {
  start_html('BP5');
  $db = db_connect('BP5.db');
  index($db);
}
elseif ($uri_ == 'Strongs') {
  start_html('Griechische Wörter des Neuen Testamentes mit deutscher Übersetzung (Strongs Nummern)');
  $db = db_connect('strongs.db');
  strongs_alle($db);
}
elseif (preg_match('/^Kapitel-(\w+)-(\d+)$/', $uri_, $m)) {
  start_html(sprintf('Kapitel %s %s', $m[1], $m[2]));
  $db = db_connect('BP5.db');
  print_chapter($db, $m[1], $m[2]);
}
elseif (preg_match('/^Strongs-(G|H)(\d+)$/', $uri_, $m)) {
  $db = db_connect('BP5.db');
  show_verses_with_strongs($db, $m[1], $m[2]);
}
elseif (preg_match('/^tq84-Strongs-(G|H)(\d+)$/', $uri_, $m)) { #_{
  $db = db_connect('BP5.db');
  tq84_show_verses_with_strongs($db, $m[1], $m[2]);
} #_}
elseif (preg_match('/^Haeufige-Woerter-Neues-Testament/', $uri_, $m)) { #_{
  frequent_words_nt();
} #_}
elseif (preg_match('/^Strongs-(\d+)$/', $uri_, $m)) {
  header('Location: Strongs-G' . $m[1], 301);
  exit(0);
}
else {
  print "oh no: $uri_!";
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

  print "<hr>";

  print "<a href='Haeufige-Woerter-Neues-Testament'>Häufige Wörter im Neuen Testament</a>";

  print "</body></html>";

} #_}

function strongs_alle($db) { #_{

  $res = db_prep_exec_fetchall($db, 'select nr, word, word_de from strongs order by nr', array());

  if (! $res) {
    print("Well...<br>");
    exit(1);
  }

  print("<table>");
  foreach ($res as $row) {
    printf("<tr><td><a href='Strongs-%s'>%s</a></td><td>%s</td></tr>", $row['nr'], $row['word'], $row['word_de']);
  }
  print("</table>");

} #_}

function show_verses_with_strongs($db, $G_or_H, $nr) { #_{

  $nr_G_or_H = "$G_or_H$nr";

  $db_strongs = db_connect('strongs.db');
  $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word, word_de, strongs_en, strongs_de from strongs where nr = ?', array($nr_G_or_H));


  $word_de = $row_strongs['word_de'];
  $word = $row_strongs['word'];
  start_html(sprintf('Strongs Nummer %d (%s - <i>%s</i>)', $nr, $word, $word_de));

  $strongs_en = $row_strongs['strongs_en'];

  $strongs_de = $row_strongs['strongs_de']; # Google Übersetzung
  $strongs_de = preg_replace_callback('/(G)(\d+)/',
    function($m) use ($db_strongs) {
      $strongs_nr_ = $m[1] . str_pad($m[2], 4, '0', STR_PAD_LEFT);
       $row_strongs_ = db_prep_exec_fetchrow($db_strongs, 'select word from strongs where nr = ?', array($strongs_nr_));
       return "<a href='Strongs-$strongs_nr_'>" . $row_strongs_['word'] . "</a>";
    },
    $strongs_de
    );


  print "Strong's Eintrag:";
  print "<pre style='background-color:#c9ffaf; border:1px solid black'><code>" . $strongs_en . "</code></pre>";

  print "Google-Übersetzung vom Strong's-Eintrag:";
  print "<pre style='background-color:#c9faff; border:1px solid black'><code>" . $strongs_de . "</code></pre>";

  print "<hr>";

  $res_strongs_see = db_prep_exec_fetchall($db_strongs, 'select nr_2 from strongs_see where nr_1 = ?', array($nr_G_or_H));
  foreach ($res_strongs_see as $row_strongs_see) {
    $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word, word_de from strongs where nr = ?', array($row_strongs_see['nr_2']));
    printf ("<br><a href=\"Strongs-%s\">%s: %s</a>", $row_strongs_see['nr_2'], $row_strongs['word'], $row_strongs['word_de']);
  }


  print "<h2>Siehe auch</h2>";

  printf("<h2>Verse, die %s enthalten</h2>", $word);

  print("Achtung, zur Zeit werden wegen Performancegründen nur die ersten 50 Verse angezeigt");

  print "
   <div id='canvas'>
</div>
<script>function init() {
   let d = document.getElementById('canvas');
   d.style.width = '20cm';
   d.style.position = 'relative';
   let lw = new tq84.line_writer(d, '20cm', {start_from_top_px: 30 });

";


  $res_1 = db_prep_exec_fetchall($db, 'select distinct v_id, b, c, v from word_v where strongs = ? order by v_id limit 50', array($nr_G_or_H));

  foreach ($res_1 as $row_1) {

    printf("lw.emit('<a href=\"Kapitel-%s-%d\">%s-%d-%d</a>:<br><a href=\"/Biblisches/Kommentare/%s_%s.html#I%s-%s-%s\">dt.</a>');\n",
      $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v'],
      $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v']);


    $res_2 = db_prep_exec_fetchall($db, '
      select
        strongs, txt, parsed
      from
        word
      where
        v = ?
      order by
        no
       ', array($row_1['v_id'])
    );


    foreach ($res_2 as $row_2) {

      $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word_de from strongs where nr = ?', array($row_2['strongs']));

      if ($row_2['strongs'] == $nr_G_or_H) {
        $b = '<b style="color:#cc5300">';
        $b_ = '</b>';
      }
      else{
        $b = $b_ = '';
      }

      printf("lw.emit('$b%s$b_<br>" .
             "<span class=\"parsed\">%s</span><br>" .
             "<span class=\"word_de\">%s</span><br>" .
             "<a class=\"strong\" href=\"Strongs-%s\">%s</a>');\n",
        to_greek_letters($row_2['txt']),
        $row_2['parsed'],
        $row_strongs['word_de'],
        $row_2['strongs'], $row_2['strongs']
      );


    }


  }

  print(" d.style.height = (lw.height() + 120 ) + 'px'; ");
  print ("}\n</script>\n");

  print("<hr><a href='Strongs'>Alle Strongs Nummern</a>");


} #_}

function frequent_words_nt() { #_{

  start_html('Häufige Wörter im Neuen Testament');

  $db_bp5 = db_connect('BP5.db'); 
  $db_strongs = db_connect('strongs.db');
  print ("<table>");
  $res_cnt = db_prep_exec_fetchall($db_bp5, 'select count(*) cnt, strongs, txt from word group by strongs order by count(*) desc limit 50');

  foreach ($res_cnt as $row_cnt) {

    $nr_G_or_H = $row_cnt['strongs'];
    $strongs_rec = strongs_nr_to_rec($db_strongs, $nr_G_or_H);

#   print "nr_G_or_H: $nr_G_or_H - ";
#   print $row_cnt['cnt'];
#   print " - ";
#   print to_greek_letters($row_cnt['txt']);
#   print "<br>";

    printf("<tr>" . 
      "<td>%d</td>" . 
      "<td>%s</td>" .
      "<td>%s</td></tr>",
      $row_cnt['cnt'],
      sprintf('<a href="Strongs-%s">%s</a>', $nr_G_or_H, to_greek_letters($row_cnt['txt'])),
      $strongs_rec['word_de']
    );

  }

  print ("</table>");

  print ("<h2>Siehe auch</h2>");
  print ("<a href='https://renenyffenegger.ch/Biblisches/Sprachen/Griechisch-Neues-Testament-bekannt.html'>Bekannte Griechische Wörter des Neuen Testamentes</a>");

  print "</body></html>";

} #_}

function print_chapter($db, $abbr, $c) { #_{

  $res = db_prep_exec_fetchall($db, 'select strongs, v, word, parsed from word_v where b=? and c=? order by no', array($abbr, $c));

  if (! $res) {
    print("hmm, what now?<br>");
    exit(1);
  }

  print "<table border=1>";
  foreach ($res as $row) {
    printf ("<tr><td>%d</td><td><a href='Strongs-%s'>%s</a></td><td>%s</td></tr>",  $row['v'], $row['strongs'], to_greek_letters($row['word']), $row['parsed']);
  }
  print "</table>";

  print "<p><a href='index'>Inhaltsverzeichnis</a>";
} #_}

function strongs_nr_to_rec($db_strongs, $nr_G_or_H) { #_{

  $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word, word_de, strongs_en, strongs_de from strongs where nr = ?', array($nr_G_or_H));

  return $row_strongs;
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

function start_html($title) { #_{
   print "<!DOCTYPE html>
  <html>
  <head>
  <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
  <! -- meta name='description' content='' / -->
  <title>$title</title>
  <style>

    a.strong {font-size: 70%}
   .parsed   {font-size: 80%; color: #339;}

  </style>
  <script type='text/javascript' src='/requisites/js/line_writer.js'></script>
  </head>
  <body onload='init()'><h1>$title</h1>
";

} #_}

?>
