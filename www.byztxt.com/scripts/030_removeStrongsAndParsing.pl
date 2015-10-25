use warnings;
use strict;

my $in_dir  = '../out/010_oneLinePerVerse';
my $out_dir = '../out/030_removeStrongsAndParsing';

opendir (my $in_dir_h, $in_dir) or die;

while (my $ed = readdir($in_dir_h)) {
  next if substr($ed, 0, 1) eq '.';

  do_edition($ed);
}
closedir($in_dir_h);


sub do_edition { # {{{

  my $ed = shift;

# die unless -f "$in_dir/$ed";

  open (my $f, '<', "$in_dir/$ed" ) or die "could not open $in_dir/$ed";
  open (my $o, '>', "$out_dir/$ed") or die "could not open $out_dir/$ed";

  while (my $line = <$f>) {

  # Just checking, if there is book-chapter-verse, followed
  # by a bar:
    die unless $line =~ m!([^-]+-\d+-\d+)\|(.*)!;

    my $verse_ident = $1;
    my $text        = $2;

    $text =~ s/{[^}]*}//g;
    $text =~ s/\d+//g;
    $text =~ s/ +/ /g;
    $text =~ s/ *$//g;

    print $o "$verse_ident|$text\n";

  }


  close($o);
  close($f);

} # }}}
