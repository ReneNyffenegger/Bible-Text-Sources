use warnings;
use strict;
use utf8;

use DBI;

my $in_dir  = '../out/010_oneLinePerVerse';
my $out_dir = '../out/040_createDB';


opendir (my $in_dir_h, $in_dir) or die;

while (my $edition = readdir($in_dir_h)) {
  next if substr($edition, 0, 1) eq '.';

  next unless $edition eq 'BP05FNL';

  do_edition($edition);
}
closedir($in_dir_h);

sub do_edition { # {{{

  my $edition = shift;

  my $dbh = create_new_db ("$out_dir/$edition.db");

  create_schema($dbh, $edition);

  fill_db($dbh, $edition);

  $dbh -> disconnect;

} # }}}

sub fill_db { # {{{

  my $dbh     = shift;
  my $edition = shift;

  open(my $text_h, '<', "$in_dir/$edition") or die $!;

  my $sth = $dbh -> prepare('insert into bible values (:book, :chapter, :verse, :word_cnt, :word_greek, :strong_nr_1, :strong_nr_2, :parsed_1, :parsed_2)');
  $dbh->begin_work or die $!;

  my $word_cnt  = 0;
  my $verse_cnt = 0;

  while (my $text_in = <$text_h>) { # {{{

    $verse_cnt ++;
    my ($book, $chapter, $verse, $text) = $text_in =~ m!([^-]+)-(\d+)-(\d+)\|(.*)!;

    $text = remove_alternatives($text);

    while ($text) {

      my $word_latin = '';
      my $strong_nr_1 = 0;
      my $strong_nr_2 = 0;
      my $parsed_1;
      my $parsed_2;

      if ($text =~ s!^([a-zA-Z]+) *!!) { # mt-6-24, last word
         $word_latin = $1;
      }
      if ($text =~ s!^(\d+) *!!) { # {{{ 

        $strong_nr_1 = $1;

        if ($text =~ s!^(\d+) *!!) { # {{{
          $strong_nr_2 = $1;
        } # }}}
        if ($text =~ s!^{([^}]+)} *!!) { # {{{
          $parsed_1 = $1; 

          if ($text =~ s!^{([^}]+)} *!!) { # {{{
            $parsed_2 = $1; 
          } # }}}

        } # }}}
        else { # {{{
          die;
        } # }}}

      } # }}}
      else {
         die $text;
      }
      $word_cnt ++;
#     printf "%-20s %5d %5d %-10s %-10s\n", $word_latin, $strong_nr_1, defined $strong_nr_2 ? $strong_nr_2 : 0, $parsed_1, defined $parsed_2 ? $parsed_2 : '';

      my $word_greek = $word_latin;
      $word_greek =~ tr/abcdefghiklmnoprstuvwxyz/αβχδεφγηικλμνοπρστυςωξθζ/;
      $sth -> execute($book, $chapter, $verse, $word_cnt, $word_greek, $strong_nr_1, $strong_nr_2, $parsed_1, $parsed_2) or die $!;

    }

    die if length($text);

  } # }}}

  $dbh->commit;

  if ($edition eq 'BP05FNL') {
     die "Expected 7957 inserted words, but actually did $verse_cnt" unless $verse_cnt == 7957;
  }
  print "Inserted: $verse_cnt verses, $word_cnt words\n";

  close $text_h;
} # }}}

sub create_new_db { # {{{

  my $db_file = shift;

  print "$db_file";

  if (-f $db_file) {
    print " [delete]";
    unlink $db_file or die $!;
  }

  print "\n";

  my $dbh = DBI->connect("dbi:SQLite:dbname=$db_file") or die "Could not create the.db $!";

  return $dbh;

} # }}}

sub create_schema { # {{{
  my $dbh = shift;

  $dbh -> do ('create table bible (
      book              varchar,
      chapter           number,
      verse             number,
      word_cnt          number,
      word_greek        varchar,
      strong_nr_1       number,
      strong_nr_2       number,
      parsed_1          varchar,
      parsed_2          varchar)') or die $!;

   $dbh -> do('create index bible_ix_book_chapter_verse on bible(book, chapter, verse)');

} # }}}

sub remove_alternatives { # {{{

  my $text = shift;

  $text =~ s/\|([^|]+)\|[^|]+\|/$1/g if $text =~ m!\|!;

  die $text if $text =~ /\|/;
  return $text;

} # }}}
