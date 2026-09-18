#!/usr/bin/perl -w 
# Find and calculate length of poly-N stretches in sequences.
# Input is nucleotide dataset.
# Output is table: sequence_ID, sequence, length
# Written for Yvonne 1 Sep 2026, Tomas Larsson

use strict;
use warnings;
use diagnostics;

my$sequenceFile = $ARGV[0];
my$sequence = "";
my$currentID = "";

my @substrings = "";

print "sequence_id" . "\t" . "sequence" . "\t" . "length" . "\t" . "homopolymer_type" . "\n";
open INFILE, "$sequenceFile" or die "Could not open file: $! \n";

while(my$line = <INFILE>) {
  chomp $line;
  if ($line =~ />/) {
    push (@substrings, $&) while($sequence =~ m/([a|A]*|[c|C]*|[g|G]*|[t|T]*|[n|N]*)/g);
    foreach (@substrings) {
    chomp$_;
      unless ($_ eq "" or length($_) < 2) { 
        print "$currentID" . "\t" . $_ . "\t" . length($_) . "\t" . "poly-". substr($_, 0, 1) . "\n";
      }
    }
    #print "\n";
    $line =~ s/>//;
    $currentID = $line;
    #print $line . "\n";
    $sequence = "";
    @substrings = "";
  } else {
    $sequence = $sequence . $line;
  }
}

#Take care of the last record, ugly but works.
push (@substrings, $&) while($sequence =~ m/([a|A]*|[c|C]*|[g|G]*|[t|T]*|[n|N]*)/g);
    foreach (@substrings) {
    chomp$_;
      unless ($_ eq "" or length($_) < 2) { 
        print "$currentID" . "\t" . $_ . "\t" . length($_) . "\t" . "poly-". substr($_, 0, 1) . "\n";
      }
    }
close INFILE;
exit;
