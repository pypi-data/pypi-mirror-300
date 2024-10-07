N I X M
=======


**NAME**

::

   NIXM - Nix Em.


**SYNOPSIS**

::

    nixm  <cmd> [key=val] [key==val]
    nixmc [-i] [-v]
    nixmd
    nixms


**DESCRIPTION**

::

    NIXM can connect to IRC, fetch and display RSS feeds, take todo
    notes and log text. You can also copy/paste the service file and
    run it under systemd for 24/7 presence in a IRC channel.


**INSTALL**


installation is done with pipx

::

    $ pipx install nixm
    $ pipx ensurepath


**USAGE**


without any argument the bot does nothing

::

    $ nixm
    $

see list of commands

::

    $ nixm cmd
    cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,
    pwd,rem,req,res,rss,srv,syn,tdo,thr,upt


start a console

::

    $ nixmc
    >


use -v to enable verbose

::

    $ nixmc -v
    NIXM since Tue Sep 17 04:10:08 2024
    > 


use -i to init modules

::

    $ nixmc -i
    >



start daemon

::

    $ nixmd
    $


start service

::

   $ nixms
   <runs until ctrl-c>


**CONFIGURATION**


*irc*

::

    $ nixm cfg server=<server>
    $ nixm cfg channel=<channel>
    $ nixm cfg nick=<nick>

*sasl*

::

    $ nixm pwd <nsvnick> <nspass>
    $ nixm cfg password=<frompwd>4

*rss*

::
 
    $ nixm rss <url>
    $ nixm dpl <url> <item1,item2>
    $ nixm rem <url>
    $ nixm nme <url> <name>

*opml*

::

    $ nixm exp
    $ nixm imp <filename>


**SYSTEMD**

::

    $ nixm srv > nixm.service
    $ sudo mv nixm.service /etc/systemd/system/
    $ sudo systemctl enable nixm --now

    joins #nixm on localhost


**COMMANDS**

::

    here is a list of available commands

    cfg - irc configuration
    cmd - commands
    dpl - sets display items
    err - show errors
    exp - export opml (stdout)
    imp - import opml
    log - log text
    mre - display cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    res - restore deleted feeds
    rss - add a feed
    srv - create service file
    syn - sync rss feeds
    tdo - add todo item
    thr - show running threads


**SOURCE**

::

    source is at ``https://github.com/otpcr/nixm``


**FILES**

::

    ~/.nixm
    ~/.local/bin/nixm   (cli)
    ~/.local/bin/nixmc  (console)
    ~/.local/bin/nixmd  (daemon)
    ~/.local/bin/nixms  (service)
    ~/.local/pipx/venvs/nixm/*


**AUTHOR**

::

    Bart Thate <record11719@gmail.com>


**COPYRIGHT**

::

    NIXM is Public Domain.
