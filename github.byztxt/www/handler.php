<?php


$uri = $_SERVER['REQUEST_URI'];

# Get uri's last portion:
$uri_ = end(explode('/', $uri));

# print_r(SQLite3::version());

if ($uri_ == 'index') { #_{
  start_html('BP5');
  $db = db_connect('BP5.db');
  index($db);
} #_}
elseif ($uri_ == 'Strongs') { #_{
  header('Location: Strongs-Griechisch' . $m[1], 301);
  exit(0);
} #_}
elseif ($uri_ == 'Strongs-Griechisch') { #_{
  $db = db_connect('strongs.db');
  strongs_alle($db, 'G');
} #_}
elseif ($uri_ == 'Strongs-Hebraeisch') { #_{
  $db = db_connect('strongs.db');
  strongs_alle($db, 'H');
} #_}
elseif (preg_match('/^Kapitel-(\w+)-(\d+)$/', $uri_, $m)) { #_{
# start_html(sprintf('Kapitel %s %s', $m[1], $m[2]));
  print_chapter($m[1], $m[2]);
} #_}
elseif (preg_match('/^Strongs-(G|H)(\d+)$/', $uri_, $m)) { #_{
  show_verses_with_strongs($m[1], $m[2]);
} #_}
elseif (preg_match('/^tq84-Strongs-(G|H)(\d+)$/', $uri_, $m)) { #_{
  $db = db_connect('BP5.db');
  tq84_show_verses_with_strongs($db, $m[1], $m[2]);
} #_}
elseif (preg_match('/^Haeufige-Woerter-Neues-Testament/', $uri_, $m)) { #_{
  frequent_words_nt();
} #_}
elseif (preg_match('/^Strongs-(\d+)$/', $uri_, $m)) { #_{
  header('Location: Strongs-G' . $m[1], 301);
  exit(0);
} #_}
else { #_{
  print "oh no: $uri_!";
} #_}


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

function strongs_alle($db, $G_or_H) { #_{

  $class_table = '';
  $title = 'Griechische Wörter des Neuen Testamentes mit deutscher Übersetzung (Strongs Nummern)';
  if ($G_or_H == 'H') {
    $class_table = ' class="all-hebr-strongs"';
    $title = 'Hebräische Wörter des Neuen Testamentes mit deutscher Übersetzung (Strongs Nummern)';
  }

  start_html_title($title);

  print("\n<style>
   table.all-hebr-strongs td:nth-child(2) {text-align: right}

   @media screen and (max-width: 1000px) {
     td { font-size: 1.4em; }
   }

</style>\n");

  print("</head><body>\n");

  print("<h1>$title</h1>\n");

  $res = db_prep_exec_fetchall($db, 'select nr, word, word_de from strongs where nr like ? order by nr', array("$G_or_H" . '%'));

  if (! $res) {
    print("Well...<br>");
    exit(1);
  }


  print("<table$class_table>");
  foreach ($res as $row) {
    printf("<tr><td><a href='Strongs-%s'>%s</a></td><td>%s</td><td>%s</td></tr>", $row['nr'], $row['nr'], $row['word'], $row['word_de']);
  }
  print("</table>");

} #_}

function css_hebr_font_face() { #_{
  print ("
      @font-face {
        font-family: SBL-Hebrew;
        src: url(https://renenyffenegger.ch/font/SBL_Hbrw.woff2) format('woff2'   );
        src: url(https://renenyffenegger.ch/font/SBL_Hbrw.woff)  format('woff'    );
        src: url(https://renenyffenegger.ch/font/SBL_Hbrw.ttf)   format('truetype');
      }
  ");

} #_}

function css_verses($G_or_H) { #_{

  $left_right = 'left';
  $ltrtr      = 'ltr';

  
  $font_face_txt = '';
  if ($G_or_H == 'H') {
    $left_right = 'right';
    $ltrtr      = 'rtl';

    $font_face_txt = "font-family: SBL-Hebrew;";
    css_hebr_font_face();

  }


  print("

   #css_verses_container {
     width: 60em;
     direction: $ltrtr;
   }

   .css_word_box {
      float: $left_right;
      padding: 0.25em;
      height: 9em
    }


   .css_verse_id {
     float: $left_right;
     position:absolute;
     $left_right: 0;
    }


   .css_verse {
      text-align: $left_right;
      position: relative;
      padding-$left_right: 5em; /* Adjust indentation here */
      margin-bottom: 20px;
      display: table;
    }

   .css_verse_break {
      clear:both;
    }


    a.strong   {font-size: 70%}
   .txt        {
      display: block: height: 2em;
      font-size: 1.4em; $font_face_txt
    }
   .parsed     {display: block; height: 2em; font-size: 80%; color: #339;}
   .word_de    {display: block; height: 2em; font-size: 80%; color: #933;}
   .css_strong {display: block; height: 2em; }
/*   table.all-hebr-strongs td:nth-child(2) {text-align: right} */

   @media screen and (max-width: 960px) {
     #css_verses_container {
        width: 360px;
     }
   }
  ");

 

} #_}

function show_verses_with_strongs($G_or_H, $nr) { #_{

  $nr_G_or_H = "$G_or_H$nr";

  $db_strongs = db_connect('strongs.db');

  if ($G_or_H == 'G') {
    $db = db_connect('BP5.db');
  }
  else {
    $db = db_connect('wlc.db');
  }

  $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word, word_de, note_de, strongs_en, strongs_de from strongs where nr = ?', array($nr_G_or_H));


  $word_de = $row_strongs['word_de'];
  $word = $row_strongs['word'];
  $word_styled;
  if ($G_or_H == 'G') {
    $word_styled = $word;
#   $title = sprintf('Strongs Nummer %d (%s - <i>%s</i>)', $nr, $word, $word_de);
  }
  else {
    $word_styled = "<span style='font-family:SBL-Hebrew'>$word</span>";
#   $title = sprintf('Strongs Nummer %d (<span style="font-family:SBL-Hebrew">%s</span> - %s)', $nr, $word, $word_de);
  }

  $title = sprintf('Strongs Nummer %d (%s - <i>%s</i>)', $nr, $word_styled, $word_de);
  start_html_title($title);

  print("\n<style>\n");
  css_verses($G_or_H);
  print("\n</style>\n");

  print ("</head><body>\n");

  print ("<h1>$title</h1>");


  $strongs_en = $row_strongs['strongs_en'];

  $strongs_de = $row_strongs['strongs_de']; # Google Übersetzung

  $strongs_de = replace_GH_numbers($strongs_de, $db_strongs);

  print "Englischer Eintrag für die Strong Nummer:";
  print "<pre style='background-color:#c9ffaf; border:1px solid black'><code>" . $strongs_en . "</code></pre>";

  print "Deutsche Google-Übersetzung:";
  print "<pre style='background-color:#c9faff; border:1px solid black'><code>" . $strongs_de . "</code></pre>";

  print "<hr>";

  $note_de = $row_strongs['note_de'];
  if ($note_de != NULL) {
    print(replace_signum_sectionis(replace_GH_numbers($note_de, $db_strongs)));
    print "<hr>";
  }

  #_{ See also
  


  $see_also_first = true;
  $res_strongs_see = db_prep_exec_fetchall($db_strongs, 'select e.id, s.description from strongs_see s join strongs_see_entry e on s.id = e.id where e.nr = ?', array($nr_G_or_H));
  foreach ($res_strongs_see as $row_strongs_see) {

    if ($see_also_first) {
      $see_also_first = false;
      print("<h2>Siehe auch</h2>");
    }

    $res_strongs_see_entry = db_prep_exec_fetchall($db_strongs, 'select nr from strongs_see_entry where id = ?', array($row_strongs_see['id']));
    printf("<b>%s</b><ul>", $row_strongs_see['description']);
    foreach ($res_strongs_see_entry as $row_strongs_see_entry) {

      print("<li>" . strong_nr_to_html_link($row_strongs_see_entry['nr'], $db_strongs));
        
    }
    print("</ul>");

  }
  if (! $see_also_first) {
    print("<hr>");
  }

  #_}
  #_{ Synonyms
  


  $syn_first = true;
  $res_strongs_syn = db_prep_exec_fetchall($db_strongs, 'select e.id, s.short, s.description from strongs_syn s join strongs_syn_entry e on s.id = e.id where e.nr = ?', array($nr_G_or_H));
  foreach ($res_strongs_syn as $row_strongs_syn) {

    if ($syn_first) {
      $syn_first = false;
      print("<h2>Synonyme</h2>");
    }

    $res_strongs_syn_entry = db_prep_exec_fetchall($db_strongs, 'select nr from strongs_syn_entry where id = ?', array($row_strongs_syn['id']));
    print("<ul>");
    foreach ($res_strongs_syn_entry as $row_strongs_syn_entry) {

      print("<li>" . strong_nr_to_html_link($row_strongs_syn_entry['nr'], $db_strongs));
        
    }
    print("</ul>");
    printf("%s\n", $row_strongs_syn['description']);

  }
  if (! $syn_also_first) {
    print("<hr>");
  }

  #_}

  #_{ Show root of strongs
  
  $res_strongs_root = db_prep_exec_fetchall($db_strongs, 'select root from strongs_root where nr = ?', array($nr_G_or_H));
  $first_root = true;
  foreach ($res_strongs_root as $row_strongs_root) {
    if ($first_root) {
      $first_root = false;
      print("<hr>Wurzel(n) von $word ist/sind:<ul> ");
    }
#   else {
#     print(" - ");
#   }
 #  print (replace_GH_numbers($row_strongs_root['root'], $db_strongs));
      print("<li>" . strong_nr_to_html_link($row_strongs_root['root'], $db_strongs));
  }
  if (! $first_root) {
    print("</ul>");
  }


  #_}
  #_{ Show strongs of which word is root

  $res_strongs_toor = db_prep_exec_fetchall($db_strongs, 'select nr from strongs_root where root = ?', array($nr_G_or_H));
  $first_toor = 1;
  foreach ($res_strongs_toor as $row_strongs_toor) {
    if ($first_toor) {
      print("<hr>$word is Wurzel von: <ul>");
      $first_toor = 0;
    }
#   else {
#     print(" - ");
#   }
#   print (replace_GH_numbers($row_strongs_toor['nr'], $db_strongs));
      print("<li>" . strong_nr_to_html_link($row_strongs_toor['nr'], $db_strongs));
  }
  if (! $first_toor) {
    print("</ul>");
  }
  #_}



  printf("<h2>Verse, die %s enthalten</h2>", $word_styled);

# print("<i>Achtung, zur Zeit werden wegen Performancegründen nur die ersten 100 Verse angezeigt.</i><p>");


  $left_to_right = true;
  if ($G_or_H == 'H') {
    $left_to_right = false;
  }

// emit_verses_2
//  canvas_and_init_and_opened_script($left_to_right);
  
// $style_rtl = '';
// if (! $left_to_right) {
//   $style_rtl = ' style="direction:rtl"';
// }

# print("\n\n<div id='css_verses_container'>");

  $res_1 = db_prep_exec_fetchall($db, 'select distinct v_id, b, c, v from word_v where strongs = ? order by v_id limit 100', array($nr_G_or_H));

  //emit_verses($res_1, $db, $db_strongs, $nr_G_or_H);
  emit_verses_2($res_1, $db, $db_strongs, $nr_G_or_H, 100);
  // emit_verses_2:
# print("</div> <!-- css_verses_container -->\n");
# print("<div style='clear:left;float:left'>");

  if ($G_or_H == 'H') {
    print("<hr>Parsing Information (<a href='http://openscriptures.github.io/morphhb/parsing/HebrewMorphologyCodes.html'>Morphologie-Codes</a>) und Lemma-Daten sind unter <a href='https://creativecommons.org/licenses/by/4.0/'>CC BY 4.0</a> veröffentlicht und stammen aus dem <a href='http://openscriptures.github.io/morphhb/index.html'>OpenScriptures Hebrew Bible</a> Projekt.");
  }

  print("<hr><a href='Strongs-Griechisch'>Alle Griechischen Strongs Nummern</a> / <a href='Strongs-Hebraeisch'>Alle Hebräischen Strongs Nummern</a>");

# print ("</div>");


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

function print_chapter($abbr, $c) { #_{

  $books_db = db_connect('BibleBooks.db'); # Created by https://github.com/ReneNyffenegger/Biblisches/blob/master/db/create-db.py

  $book_row = db_prep_exec_fetchrow($books_db, 'select testament from book where id = ?', array($abbr));

  $testament = $book_row['testament'];


  if ($testament == 'new') {
    $G_or_H = 'G';
#   $left_to_right = true;
    $db_text = db_connect('BP5.db');
  }
  else {
    $G_or_H = 'H';
#   $left_to_right = false;
    $db_text = db_connect('wlc.db');
  }
  $title = sprintf('Kapitel %s %s', $abbr, $c);
  start_html_title($title);
  print("\n<style>\n");
  css_verses($G_or_H);
  print("\n</style>\n");
  print ("</head><body>\n");

  print("<h1>$title</h1>");

  $res = db_prep_exec_fetchall($db_text, 'select distinct v_id, c, b, v from word_v where b=? and c=? order by v_id', array($abbr, $c));

  if (! $res) {
    print("hmm, what now?<br>");
    exit(1);
  }
//is_tq_browser();

 // canvas_and_init_and_opened_script($left_to_right);
#print("\n\n<div id='css_verses_container'>");
  $db_strongs = db_connect('strongs.db');

  emit_verses_2($res, $db_text, $db_strongs, 'n/a', 999999);
  # print("</div> <!-- css_verses_container -->\n");

# print "<table border=1>";
# foreach ($res as $row) {
#   printf ("<tr><td>%d</td><td><a href='Strongs-%s'>%s</a></td><td>%s</td></tr>",  $row['v'], $row['strongs'], to_greek_letters($row['word']), $row['parsed']);
# }
# print "</table>";

  # print("<div style='clear:left;float:left'>");
//print "</script>";

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

function start_html_title($title) {
  $title = strip_tags($title);

   print("<!DOCTYPE html>
<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
<meta name='viewport' content='width=device-width, initial-scale=1'>
<!-- meta name='description' content='' / -->
<title>$title</title>
");
}

function start_html($title) { #_{

  start_html_title($title);

  print("<style>

    /*
   .css_verse_id,
   .css_word_box {
      float: left;
      padding: 9em;
      height: 9em
    }
*/

   #css_verses_container {
      width: 60em;
   }

    a.strong   {font-size: 70%}
   .parsed     {/* display: block; height: 2em; */ font-size: 80%; color: #339;}
   .word_de    {/* display: block; height: 4em; */ font-size: 80%; color: #933;}
   .css_strong {/* display: block; height: 6em; */ }

   @media screen and (max-width: 1000px) {
     #css_verses_container {width: 400px;}
   }

   

  </style>
  <script type='text/javascript' src='/requisites/js/line_writer.js'></script>
  </head>
  <body onload='init()'><h1>$title</h1>
");

} #_}

function canvas_and_init_and_opened_script($left_to_right) { #_{
  #
  # When calling canvas_and_init_and_opened_script(), it writes a <script> tag
  # but no </script> tag! This must be done by the caller!
  #

  $left_to_right_ = '';
  if (! $left_to_right) {
     $left_to_right_ = ', left_to_right: 0';
  }

  print "
   <div id='canvas'>
</div>
<script>function init() {
   let d = document.getElementById('canvas');
   d.style.width = '20cm';
   d.style.position = 'relative';
   let lw = new tq84.line_writer(d, '20cm', {start_from_top_px: 30 $left_to_right_ });

";

} #_}

function emit_verses($res_1, $db_text, $db_strongs, $nr_G_or_H_highlight) { #_{

    $first_verse = 1;
    foreach ($res_1 as $row_1) { #_{

      if (! $first_verse) {
        printf("lw.new_line();\n");
      }
      else {
        $first_verse = 0;
      }

      $kommentar_url = sprintf("/Biblisches/Kommentare/%s_%s.html#I%s-%s-%s", $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v']);
      if (is_tq_browser) {
         $kommentar_url = "http://localhost" . $kommentar_url;
      }



    printf("lw.emit('<a href=\"Kapitel-%s-%d\">%s %d:%d</a>:<br><a href=\"$kommentar_url\">dt.</a>');\n",
      $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v'] #,
      #     $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v']
      );

    $res_2 = db_prep_exec_fetchall($db_text, '
      select
        strongs, txt, parsed
      from
        word
      where
        v = ?
      order by
        order_
       ', array($row_1['v_id'])
    );


    foreach ($res_2 as $row_2) {

      $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word_de from strongs where nr = ?', array($row_2['strongs']));

      if ($row_2['strongs'] == $nr_G_or_H_highlight) {
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
  } #_}

  print(" d.style.height = (lw.height() + 120 ) + 'px'; ");
  print ("}\n</script>\n");

} #_}

function emit_verses_2($res_1, $db_text, $db_strongs, $nr_G_or_H_highlight, $max_verse_cnt) { #_{
    print("\n\n<div id='css_verses_container'>");

#   $first_verse = 1;
    $verse_cnt   = 0;
    foreach ($res_1 as $row_1) { #_{

      $verse_cnt ++;

#     if (! $first_verse) {
      if ($verse_cnt == 1) {
        print("\n<div class='css_verse_break'></div>\n");
      }
#     else {
#       $first_verse = 0;
#     }
      

      $kommentar_url = sprintf("/Biblisches/Kommentare/%s_%s.html#I%s-%s-%s", $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v']);
      if (is_tq_browser()) {
         $kommentar_url = "http://localhost" . $kommentar_url;
      }

      print("\n <div class='css_verse'>\n");
      printf("\n  <span class='css_verse_id'><a href=\"Kapitel-%s-%d\">%s %d:%d</a>:<br><a href=\"$kommentar_url\">dt.</a></span>",
        $row_1['b'], $row_1['c'], $row_1['b'], $row_1['c'], $row_1['v'] #,
      );

    $res_2 = db_prep_exec_fetchall($db_text, '
      select
        strongs, txt, parsed
      from
        word
      where
        v = ?
      order by
        order_
       ', array($row_1['v_id'])
    );


    foreach ($res_2 as $row_2) {

      $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word_de, flag from strongs where nr = ?', array($row_2['strongs']));

      if ($row_2['strongs'] == $nr_G_or_H_highlight) {
        $b = '<b style="color:#cc5300">';
        $b_ = '</b>';
      }
      else{
        $b = $b_ = '';
      }

      $txtS = ''; #_{ Print translated word small and in grey if flag  == '?'
      $txtE = '';
      if ($row_strongs['flag'] == '?') {
        $txtS = '<span style="color:#678;font-size:70%%"><i>';
        $txtE = '</i></span>';
      }
      #_}


      printf("\n  <span class='css_word_box'>"       .
             "\n   <span class='txt'>$b%s$b_</span>" .
             "\n   <span class='parsed'>%s</span>" .
             "\n   <span class=\"word_de\">$txtS%s$txtE</span>" .
             "\n   <span class=\"css_strong\"><a class=\"strong\" href=\"Strongs-%s\">%s</a></span>" .
             "\n  </span>\n",
         to_greek_letters($row_2['txt']),
         $row_2['parsed'],
         $row_strongs['word_de'],
         $row_2['strongs'], $row_2['strongs']
       );

    }
    print(" </div> <!-- css_verse -->\n");
  } #_}

  print("</div> <!-- css_verses_container -->\n");
  print("<div style='clear:left;float:left'></div>");

  if ($max_verse_cnt <= $verse_cnt) {
     print("<i>Achtung, zur Zeit werden wegen Performancegründen nur die ersten $max_verse_cnt Verse angezeigt.</i><p>\n");
  }


} #_}

function replace_signum_sectionis($text) { #_{
  $text = preg_replace_callback(
    '/§([^-]+)-(\d+)-(\d+)/',
    function($m) { # use  ($var)
      $b=$m[1];
      $c=$m[2];
      $v=$m[3];
      return "<a href='/Biblisches/Kommentare/${b}_${c}.html#I$b-$c-$v'>$b $c:$v</a>";
    },
    $text
  );
  return $text;

} #_}

function replace_GH_numbers($text, $db_strongs) { #_{
  $text = preg_replace_callback('/(G|H)(\d+)/',
    function($m) use ($db_strongs) {
      $strongs_nr_ = $m[1] . str_pad($m[2], 4, '0', STR_PAD_LEFT);
       $row_strongs_ = db_prep_exec_fetchrow($db_strongs, 'select word from strongs where nr = ?', array($strongs_nr_));
       return "<a href='Strongs-$strongs_nr_'>" . $row_strongs_['word'] . "</a>";
    },
    $text
    );

  return $text;

} #_}

function strong_nr_to_html_link($nr, $db_strongs) { #_{
   $row_strongs = db_prep_exec_fetchrow($db_strongs, 'select word, word_de from strongs where nr = ?', array($nr));
   return sprintf("%s: <a href=\"Strongs-%s\">%s</a> (%s)", $nr, $nr, $row_strongs['word'], $row_strongs['word_de']);
} #_}

function is_tq_browser() { #_{
  $ua  = $_SERVER['HTTP_USER_AGENT' ];

  if ($ua == 'Mozilla/5.0 (TQ)') {
    return true;
  }
  return false;

} #_}

?>
