use warnings;
use strict;

my $in_dir = '../out/010_oneLinePerVerse';

my ($fh_ref, $fh_2_edition_ref) = open_file_handles();

compare_verses($fh_ref, $fh_2_edition_ref);

close_file_handles(@$fh_ref);

sub compare_verses { # {{{

  my $fh_ref           = shift;
  my $fh_2_edition_ref = shift;

  my @fh           = @$fh_ref;
  my %fh_2_edition = %$fh_2_edition_ref;

  my $fh_0 = shift @fh;

  print "Master: " . $fh_2_edition{$fh_0} . "\n";

  my %fh_with_errors;

  while (my $line_0 = <$fh_0>) {

    my ($verse_0) = $line_0 =~ /^([^|]+)/;

    die unless $verse_0;
    
    for my $f_ (@fh) {

      next if exists $fh_with_errors{$f_};

      my $line_ = <$f_>;
      my ($verse_) = $line_ =~ /^([^|]+)/;

      if ($verse_0 ne $verse_) {

        $fh_with_errors{$f_} = 1;
        print "Error $verse_0 vs $verse_ " . $fh_2_edition{$f_} . "\n";

      }

    }

  }

} # }}}

sub open_file_handles { # {{{

  my @fh;
  my %fh_2_edition;
  
  opendir (my $dir_h, $in_dir) or die;

  while (my $edition = readdir($dir_h)) {
    next if substr($edition, 0, 1) eq '.';
    open (my $fh, '<', "$in_dir/$edition") or die "Could not open $in_dir/$edition";
    $fh_2_edition{$fh} = $edition;
    push @fh, $fh;
  }

  return \@fh, \%fh_2_edition;

} # }}}

sub close_file_handles { # {{{
  close $_ or die $! for (@_);
} # }}}
