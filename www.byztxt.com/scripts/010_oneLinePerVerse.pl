# vim: foldmarker={{{,}}}
use warnings;
use strict;
use File::Slurp;

my $out_dir = '../out/010_oneLinePerVerse';

iterate_downloads();

sub iterate_downloads { # {{{

  my $download_dir = '../downloaded';

  opendir (my $dh, $download_dir) or die "Could not open $download_dir";

  while (my $edition = readdir($dh)) {
    next if substr($edition, 0, 1) eq '.';
    next unless -d "$download_dir/$edition";
    do_edition("$download_dir/$edition", $edition);
  }

} # }}}

sub do_edition { # {{{

  my $dir     = shift;
  my $edition = shift;

  open (my $out_file, '>', "$out_dir/$edition") or die "Could not open $out_dir/$edition";

  for my $book  # {{{
    (  {book_from => 'MT'   , book_to => 'mt'    },  # {{{
       {book_from => 'MR'   , book_to => 'mk'    },
       {book_from => 'LU'   , book_to => 'lk'    },
       {book_from => 'JOH'  , book_to => 'joh'   },
       {book_from => 'AC'   , book_to => 'apg'   },
       {book_from => 'RO'   , book_to => 'roem'  },
       {book_from => '1CO'  , book_to => '1kor'  },
       {book_from => '2CO'  , book_to => '2kor'  },
       {book_from => 'GA'   , book_to => 'gal'   },
       {book_from => 'EPH'  , book_to => 'eph'   },
       {book_from => 'PHP'  , book_to => 'phil'  },
       {book_from => 'COL'  , book_to => 'kol'   },
       {book_from => '1TH'  , book_to => '1thes' },
       {book_from => '2TH'  , book_to => '2thes' },
       {book_from => '1TI'  , book_to => '1tim'  },
       {book_from => '2TI'  , book_to => '2tim'  },
       {book_from => 'TIT'  , book_to => 'tit'   },
       {book_from => 'PHM'  , book_to => 'phim'  },
       {book_from => 'HEB'  , book_to => 'hebr'  },
       {book_from => 'JAS'  , book_to => 'jak'   },
       {book_from => '1PE'  , book_to => '1petr' },
       {book_from => '2PE'  , book_to => '2petr' },
       {book_from => '1JO'  , book_to => '1joh'  },
       {book_from => '2JO'  , book_to => '2joh'  },
       {book_from => '3JO'  , book_to => '3joh'  },
       {book_from => 'JUDE' , book_to => 'jud'   },
       {book_from => 'RE'   , book_to => 'offb'  }, # }}}
    ) {


    my $glob_pattern = "$dir/$book->{book_from}*";

    if ($edition eq 'BYZ05CCT' and $book->{book_from} eq 'AC') {
      print "Change glob pattern, because of BYZ05CCT/AC24.CCT\n";
      
      $glob_pattern = "$dir/$book->{book_from}.*";
    }
    elsif ($edition eq 'SCRIVNER' and $book->{book_from} eq 'TIT') {
      print "Change glob pattern, because of SCRIVNER/TITLES.SCR\n";
      
      $glob_pattern = "$dir/$book->{book_from}.*";
    }

    my @glob_files = glob($glob_pattern);

    if (@glob_files != 1) {

      print "Too many or little files match in $edition $book->{book_from}\n";
      for my $glob_file (@glob_files) {
        print "  $glob_file\n";
      }

      die;

    }
    
    do_book($out_file, $glob_files[0], $book->{book_to});

    } # }}}

  close $out_file;


} # }}}

sub do_book { # {{{

  my $out_file     = shift;
  my $in_file_name = shift;
  my $book_abbr    = shift;

  my $file_text=read_file($in_file_name) or die "could not slurp file $in_file_name";

  $file_text =~ s/#.*//gm;
  $file_text =~ s/^ *0*(\d+):0*(\d+) */QQQ$book_abbr-$1-$2|/gm;

  $file_text =~ s/\n//g;
  $file_text =~ s/QQQ//;
  $file_text =~ s/QQQ/\n/g;
  $file_text .= "\n";

  print $out_file $file_text;

} # }}}
