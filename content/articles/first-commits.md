Title: First commits
Date: 2014-11-25 21:57
Category: all
Authors: Tom, Gautier

Inspired by a [recent post](https://www.reddit.com/r/programming/comments/2na7dj/gits_initial_commit/) on reddit about git's first commit I checked out the first commits for a variety of projects. Git's first commit contains a concise, fantastic description of what git is and how it works. How do other projects compare?

<!-- PELICAN_END_SUMMARY -->

Beginnings are always interesting because well-known projects do not
yet have the status they'll achieve many years later. The lack of
attention means there is no pressure to be elegant, or even concise.

The initial commit is quite often a code-dump of an existing, working
project. Still, in some cases the history goes back as far as 1990
which is rather impressive.


## Go

The [first commit](https://code.google.com/p/go/source/diff?spec=svnf6182e5abf5eb0c762dddbb18f8854b7e350eaeb&name=fa9ce5d3f93b&r=f6182e5abf5eb0c762dddbb18f8854b7e350eaeb&format=side&path=/src/pkg/debug/macho/testdata/hello.b) in Go has nothing to do with Go itself, other than illustrating its heritage: It's hello-world written in b, the predecessor of c. Even the commit timestamp matches (1972).

In fact the [first 4 commits](https://code.google.com/p/go/source/list?r=fa9ce5d3f93b) are a homage to Go's heritage. The [first substantial commit](https://code.google.com/p/go/source/detail?r=4e9a5b0955321f15379f80dcc96cdb8b3eb4eb0d&name=fa9ce5d3f93b) is a preliminary version of the Go spec that already looks a lot like current Go with a few big omissions (e.g. channels aren't specced).


## PostgreSQL

PostgreSQL's [first commit](https://github.com/postgres/postgres/commit/d31084e9d1118b25fd16580d9d8c2924b5740dff) is from 1996. PostgreSQL's first release was in mid-1995 but, as I understand it, had a less liberal license at that time. The first commit is an import of the whole, working project with the liberal PostgreSQL license.


## Git

Git's [fist commit](https://github.com/git/git/commit/e83c5163316f89bfbde7d9ab23ca2e25604af290) was already discussed in depth in many places. I have fond memories of it because the description got me started on git fairly early. It was so nice that it convinced me instantly, despite being a real brain twister at the time.


## SQLite

The [first commit](http://www.sqlite.org/cgi/src/info/704b122e5308587b60b47a5c2fff40c593d4bf8f) from May 2000 is empty and says "initial empty check-in". The [second commit](http://www.sqlite.org/cgi/src/info/6f3655f79f9b6fc9fb7baaa10a7e0f2b6a512dfa) is a code-dump. The copyright notices say 1999, 2000 so I assume what the project was started in 1999.

Interestingly the code that was licensed as GPL2 back then is now in the public domain. I did not discover at what point the license changed.


##  Python

Python has [several first commits](https://hg.python.org/cpython-fullhistory/shortlog/82c7bab78bb1). It looks like they import an already functioning project between them.

People familiar with the project will recognize several components that have not changed in 25 years such as the `Lib` directory. See e.g. [this commit](https://hg.python.org/cpython-fullhistory/rev/5570dbb1ce55).


# Linux kernel

The full Linux history was re-assembled from three sources by Yoann Padioleau and can be found on [archive.org](https://archive.org/details/git-history-of-linux). There isn't really a first commit as such because Linus Torvalds released versioned tarballs on an ftp server that's [still around](ftp://www.nic.funet.fi/).

Kernel Newbies have written a nice [walk-through](http://kernelnewbies.org/Kernel001WalkThrough) of the first release so I'm going to stop here.


# Docker

Docker's first commit is from 2013. It never migrated from one version control system to another, and not using using version control in 2013 would expose your project to ridicule.

The code started as an internal project within dotCloud but was quickly moved to github. The [initial commit](https://github.com/docker/docker/commit/a27b4b8cb8e838d03a99b6d2b30f76bdaf2f9e5d) is a code-dump tagged as `0.0.3`.


# Xen

Xen is famous for running Amazon's ec2 infrastructure. The [first commit](http://xenbits.xen.org/gitweb/?p=xen.git;a=commit;h=93081dee186d6bb3e1ede0a179085b8504846896) is from 1970, which is of course a lie and likely an artifact of moving from bitkeeper to mercurial.

The first [substantial commit](http://xenbits.xen.org/gitweb/?p=xen.git;a=commit;h=4676bbf96dc88e9a70607fa79b3c83febc5dc54b) is a code dump by someone with an academic email address, hinting at the origins of the project.

The commit also contains a custom Linux called `xenolinux` which was developed for running efficiently on a Xen hypervisor.


# Apache

Apache's [first commit](https://github.com/apache/httpd/commit/5dbf830701af760e37e1e2c26212c34220516d85) hints at a migration from CVS to SVN at some point.

Interestingly all of the [early commits](https://github.com/apache/httpd/commits/trunk?page=760) add documentation and no code. It makes no sense to document a non-existing server so the code must have been somewhere at this point. Maybe it got lost during the repository migrations?


# Nginx

Nginx's [first commit](http://trac.nginx.org/nginx/changeset/0/nginx) dates
from August 2002, but as the commit message says "The first draft ideas are
dated back to 23.10.2001.". Igor Sysoev started with Subversion and switched to
Mercurial in April 2013.

The project doesn't contain a Makefile and is not complete. However the high
level ideas are already there.

The first version of Nginx was only meant to serve static files over HTTP. It
handles looking for a index.html document if a directory is requested but not
any other kind of URL rewrites.

A custom pool allocator is used to keep the memory footprint low. To this day
Nginx is still very light on memory usage.

The server supports FreeBSD, Linux and Win32 with their respective event queue
implementations (kqueue, select, aio). Maybe the plugin system comes from
having to support these multiple event queue implementations from the
beginning?

This [slideshare presentation from Igor Sysoev](http://www.slideshare.net/PHPConferenceArgentina/igor-sysoev-nginx)
contains a little more context on the origin of Nginx.


# Django

Django's [first commit](https://github.com/django/django/commit/d6ded0e91bcdd2a8f7a221f6a5552a33fe545359) from 2005 is empty. Checking the [second](https://github.com/django/django/commit/07ffc7d605cc96557db28a9e35da69bc0719611b) and [third](https://github.com/django/django/commit/ed114e15106192b22ebb78ef5bf5bce72b419d13) commit shows that this is an import from a private repository. This makes sense because the project started as the internal tool for the [Lawrence Journal-World](http://en.wikipedia.org/wiki/Lawrence_Journal-World) newspaper.

The order of of commits is mildly interesting: The first substantial commit is documentation. Documentation is a focus and a strength of the Django project to this day.
