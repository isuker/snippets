#!/usr/bin/perl
#
# Automatos Shell
#

# must turn off 
#use strict;
use warnings;
use Getopt::Long;
use Term::ReadLine;
use Data::Dumper;

our (@hosts, @celerras, @vnxes, @vnxs, @vplexes, @switches, @objects);
our ($verbose, $resourceObj, $self);

# Add new vars export to shell console
our %VAR_MAP = (
    'host'  => '@hosts',
    'file'  => '@celerras',
    'unified' => '@vnxes',
    'vnx' => '@vnxs',
    'vplex' => '@vplexes',
    'switch' => '@switches',
#   'package' => '$self'
#   'find' => '@objects',
);

our %gSettings = (

    # debug level: INFO, DEBUG, TRACE
    debug => "INFO",
    # Data dumper depth
    depth => 3,
);

sub load_testbed
{
    my $testBedfile = shift;
    
    require Automatos::AutoLog;
    require Automatos::ParseXml;
    require Automatos::Resource;

    my %testBedInfo = Automatos::ParseXml::getTestbed(filename=>$testBedfile);
    eval {
        $resourceObj = Automatos::Resource->new(%testBedInfo);
        $resourceObj->init();
    };
    if($@) {
        if ($verbose) {
           warn $@;
        }
    }

    unless($resourceObj) {
        print "[ERROR] Load test bed resource issues...\n";
        exit 1;
    }

    print "\n";

    my %device = $resourceObj->getDevice();
    while (my ($type, $value) = each %VAR_MAP) {
        if (defined $device{$type}) {
            print "####All $type variable \"$value\" => @{$device{$type}}\n";
            @hosts = @{$device{$type}} if $type eq 'host';
            @celerras = @{$device{$type}} if $type eq 'file';
            @vnxes = @{$device{$type}} if $type eq 'unified';
            @vnxs = @{$device{$type}} if $type eq 'block';
            @vplexes = @{$device{$type}} if $type eq 'vplex';
            @switches = @{$device{$type}} if $type eq 'switch';
        }
    }

    print "\n";
    Automatos::AutoLog->setScreenLogLevel($gSettings{debug});
}

sub precmd
{
    my $line = shift;
    # Hook to do sth
    return $line;
}

sub postcmd
{
    my ($stop, $line) = @_;

    # DO nothing now. Only extension interface
    return $stop;
}

sub parseline
{
    my $line = shift;

    # remove heading spaces
    $line =~ s/^ *//g;
    $line =~ s/\n//g;
    # remove tailing spaces
    $line =~ s/ *$//g;
    # remove extra spaces in the middle.
    #$line =~ s/ +/ /g;

    my ($cmd, $expr);
    # we need 2 part
    my @cakes = split(" ",$line, 2);
    if (scalar(@cakes) == 1) {
        $cmd  = "";
        $expr = $cakes[0];
    } else {
        $cmd  = $cakes[0];
        $expr = $cakes[1];
    }

    return ($cmd, $expr);
}

sub execute
{
    my $expr = shift;

    eval($expr);
    warn $@ if $@;
    unless ($@) {
        return 1;
    }

    return 0;
}

sub onecmd
{
    my $line = shift;

    my $stop = 0;
    # flag for command or shell. 1 mean command
    my $flag = 0;
    my ($cmd, $expr) = parseline($line);
    if ( $cmd eq "" )  {
        $flag = 0; # shell line
        if ($expr eq "h" || $expr eq "help") {
            help($expr);
            $stop=1;
        } else {
            # directly run this shell line
            $stop = execute($line);
        }
    } else {
        $flag = 1; # must run sub command
        my $printed = 0;
        if ($cmd eq 'l' || $cmd eq 'list') {
            $cmd = "list";
            $flag = 0;
        } elsif ($cmd eq 'p' || $cmd eq 'print') {
            $cmd = "print";
            $flag = 0;
        } elsif ($cmd eq 'x' || $cmd eq 'view') {
            $cmd = "view";
            $flag = 0;
        } elsif ($cmd eq 'f' || $cmd eq 'find') {
            $cmd = "find";
            $flag = 0;
            $printed = 1;
        } elsif ($cmd eq 'import') {
            $flag = 0;
            $printed = 1;
        } elsif ($cmd eq 'reload') {
            $flag = 0;
            $printed = 1;
        } elsif ($cmd eq 'o' || $cmd eq 'option') {
            $cmd = "option";
        } else {
            # command will run twice, don't konw how to
            # get the return value. Array, HASH, SCALAR??
            if ($flag==1) {
                # time to execute the whole shell line
                # no matter with sapces
                # same as line 131
                $stop = execute($line);
            } else {
                # unknown command here
                default($cmd);
                $stop = 1;

            }
            return $stop;
        } 
        my $func = "do_$cmd";
        my $ret = eval { $func->($expr); };
        if ($@) {
            warn $@;
            $stop = 1;
        } else {
            if (defined $ret && !$printed) {
                print $ret;
            }
        }
    }

    return $stop;

}

sub do_view
{
    my $data = shift;

    my $dumper = Data::Dumper->new([eval($data)]);
    $dumper->Deepcopy(1);
    $dumper->Indent(1);
    $dumper->Quotekeys(0);
    $dumper->Sortkeys(1);
    $dumper->Terse(1);
    $dumper->Maxdepth(int($gSettings{depth}));

    return $dumper->Dump();
}

sub _run_batch_command
{
    my $script = shift;

    open FILE, $script or die $!;
    my $lineno = 0;
    while (<FILE>) {
        $lineno++;
        chomp $_;
        # remove heading spaces
        $_ =~ s/^ *//g;
        # skip blank line and comment
        next if ($_ eq "" || $_ =~ /^#/);

        print "\n## File $script Line:$lineno Command => \"$_\", Output =>\n";
        onecmd($_);
    }
}

sub do_import
{
    my $script = shift;

    _run_batch_command($script);
}

sub do_reload
{
    my $module = shift;

    require Module::Refresh;
    require Module::Util;
    my $refresh = Module::Refresh->refresh;

    # refresh_module only support full filename of module
    my $module_full_filename = $module;
    if ($module_full_filename =~ /::/) {
        $module_full_filename = Module::Util::module_fs_path($module);
    }
    if ($verbose){
        print "[DEBUG] Start reload package \"$module_full_filename\"\n";
    }
    $refresh->refresh_module($module_full_filename);
    print "Reload Package \"$module\" done\n";

}

sub do_find
{
    my $data = shift;

    # find <$object> <$type> <$criteria> <$force>
    my ($device, $type, $criteria, $force) = split(" ", $data, 4);

    if (!$force) {
        $force = 0;
    }

    my $cmd = "$device->find(type=>\"$type\", force_sync=>$force";
    if ($criteria) {
        $cmd .= ", criteria=>{$criteria}";
    }
    $cmd .= ")";

    @objects = eval( $cmd );
    if ($@) {
        print $@;
    } else {
        if (@objects) {
            my $count = scalar(@objects);
            print '####Found objects variable: @objects. Total number: ', "$count\n";
            $VAR_MAP{'find'} = '@objects';
        } else {
            print "Not find any \"$type\" objects with \"$criteria\" criteria\n";
        }   
    }
}

sub do_print
{
    my $data = shift;

    my $out = print eval($data), "\n";

    # remove last char since of print return 1
    return substr($out,0,-1);

}

sub do_list
{
    my $data = shift;

    my $line = "";

    if ($data =~ /host/i) {
        $line = "Host    Type    IP\n";
        my $index = 0;
        foreach (@hosts) {
            $line .= "$index    ". $_->{os};
            $line .= "    ".$_->{ipv4_address};
            $line .= "\n";
            $index++;
        }
    }
    if ($data =~ /vnx/i) {

        my @array = @vnxs;
        $line = "VNX     Name    Model    Version    SPA    SPB\n";
        if ($data =~ /vnxe+/i) {
            $line = "VNXe    Name    Model    Version    SPA    SPB\n";
            @array = @vnxes;
        }
        my $index = 0;
        foreach (@array) {
            $line .= "$index    ". $_->getName();

            my ($spa) = $_->find(type=>"Sp", criteria=>{name=>qr/spa/i});
            my ($spb) = $_->find(type=>"Sp", criteria=>{name=>qr/spb/i});

            $line .= "    ".$spa->getProperty('model');
            my $revKey = "revision";
            if ($data =~ /vnxe+/i) {
                $revKey = "bios_version";
            }
            $line .= "    ".$spa->getProperty($revKey);
            $line .= "    ".$spa->getHostObject()->{ipv4_address};
            $line .= "    ".$spb->getHostObject()->{ipv4_address};
            $line .= "\n";
            $index++;
        }
    }
    if ($data =~ /var/i) {
        foreach my $value (values %VAR_MAP) {
            if ($value eq '$self') {
                my $ret = eval{$value};
                $line .= "$value\t=> $ret\n";
            } else {
                # This time all should be array var
                my @ret = eval($value);
                if (@ret) {
                    $line .= "$value\t=> @ret\n";
                }
            }
        }
    }
    
    my $out = print $line, "\n";
    # remove last char since of print return 1
    return substr($out,0,-1);
}

sub do_option
{
    my $data = shift;

    my ($cmd, $arg) = split(" ", $data, 2);

    my $msg="";
    my $backupLogLevel = $gSettings{debug};
    if ($cmd eq "show") {
        foreach (keys %gSettings) {
            $msg .= "$_ => $gSettings{$_} \n";
        }
    } else {

        if (defined $gSettings{$cmd}) {
            if ($arg) {
                $gSettings{$cmd} = $arg;
            }else {
                $msg = "Miss parameter for \"$cmd\" option";
            }
        } else {
            $msg =  "Not such settings: $cmd\n";
            $msg .= "Run \"o show\" command to see valid key\n";
        }
    }

    # update debug level ASAP
    eval {
        Automatos::AutoLog->setScreenLogLevel($gSettings{debug});
    };
    if ($@) {
        # if setting log level fail and then revert
        Automatos::AutoLog->setScreenLogLevel($backupLogLevel);
    }

    return $msg;

}

sub help
{
    my $line = shift;

    print "Automatos Interactive Shell Usage:  \n";
    print "   print |p : print variable\n";
    print "   list  |l [host|vnx|vnxe|var] : print HUTs/Array Info/available var\n";
    print "   view  |x : dump variable\n";
    print "   import [script]: load script file and then run line by line\n";
    print "   reload [module]: reload the module in runtime\n";
    print "   find [object type criteria force] : Shortcut for \$device->find API\n";
    print "   option|o [show|debug|depth]: config setting\n";
    print "     i.e\n";
    print "       o debug TRACE: change log level to TRACE, default is INFO\n";
    print "       o depth 5:     set Data::Dump max depth\n";
    print "       o show:        show configure\n";
    print "   exit|CTRL+D     : exit program\n";

}

sub default
{
    my $message = shift;
    print "Unsupport Command: $message\n";
}

###############################################
############# Main Program ####################
###############################################
sub usage
{
    print "Automatos Interactive Shell\n";
    print "Usage:  automatos-shell.pl -t testbed.xml [-s script [--shell]] \n";
    print "     -t|--testbed: Specify testbed file \n";
    print "     -s|--script:  Run command in script file \n";
    print "     -p|--package: Load Test Package \n";
    print "     -l|--level:   Debug Level (INFO, DEBUG, CMD, TRACE) while loading test bed file \n";
    print "     -i|--shell:   Enter Interactive Mode after script \n";
    print "     -h|--help:    Print this help \n";
    print "     -v|--verbose: Verbose mode \n";
    exit 1;
}

my ($testbed, $script, $package, $shell, $help, $level);
GetOptions(
    'testbed|t=s'  => \$testbed,
    'script|s=s'   => \$script,
    'level|l=s'   => \$level,
    'package|p=s'   => \$package,
    'shell|i'       => \$shell,
    'help|h'       => \$help,
    'verbose|v'       => \$verbose
);

if ($help) {
    usage();
}

# set debug level before load test bed
if (defined $level) {
    # Create a Log object
    require Automatos::AutoLog;
    my $log = Automatos::AutoLog->getLogger(__PACKAGE__);
    Automatos::AutoLog->setScreenLogLevel($level);
}

if (!defined $testbed) {
    usage();
} else {
    load_testbed($testbed);
}

# -t vplex.xml -p SSIETests::VNX2::Interoperability::Vplex::Base
if (defined $package) {

    my $cmd = "use $package";
    onecmd($cmd);

    my $name = "Automatos".$$;
    my $bootstrap = "new $package(name=>$name, resource=>\$resourceObj)";
    $self = eval( $bootstrap );
    if ($@) {
        print $@;
    } else {
        print '####Package variable: $self', " $self\n";
        $VAR_MAP{package} = '$self';
    }
}

# load command from file
if (defined $script) {

    print "Start execute comand from $script file line by line\n";
    _run_batch_command($script);

    if (!defined $shell) {
        exit;
    }
}

# For windows compatibility
if (!$ENV{"HOME"}) {
    $ENV{"HOME"} = "";
}

my $historyfile = $ENV{"HOME"}.'.phistory';
my $term = new Term::ReadLine 'Automatos Shell';

my $OUT = $term->OUT || \*STDOUT;
$SIG{INT} = sub {print $OUT "Caught CTRL+C, please use 'exit' to exit this program\n"};
$SIG{TERM} = sub {print $OUT "Caught CTRL+D, please use 'exit' to exit this program\n"};

while ( defined ($_ = $term->readline("Automatos Shell> ")) ) 
{
    chomp $_;
    next if ($_ eq "");
    my $line = precmd($_);
    my $stop = onecmd($line);
    $stop    = postcmd($stop, $line);
    if (not $stop) {
        open H, ">>$historyfile" || die "Can not open $historyfile";
        print H "$_\n" if /\S/;
        close H;
    }
    $term->addhistory($_) if /\S/;
}
