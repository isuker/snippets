#!/usr/bin/perl

use warnings;
use strict;

use threads;
use threads::shared;

my @gIOX :shared = ();

my @thread;

my @loop=(5,2);

foreach my $l (@loop) {

    print "loop $l\n";

    my $task = sub {

        print "do sth in $l task\n";
        sleep $l;

        push @gIOX, $l;
    };

    push @thread, threads->new($task);
}

foreach my $t (@thread) {

    if ($t->is_joinable()) {
        $t->join();
        print "$t is done\n";
        if (my $e=$t->error()) {
            print "$e\n";
        }
    }
    print $t->tid(), " is done\n";
}

sleep 10;
print @gIOX;

