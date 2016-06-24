#!/usr/bin/env perl
use Dancer;
use Ring::Checker;

get '/' => sub {
    "Hello There";
};

get '/hello/:name' => sub {
    "Hey ".params->{name}.", how are you?";
};

post '/new' => sub {
    "creating new entry: ".params->{name};
};

dance;
