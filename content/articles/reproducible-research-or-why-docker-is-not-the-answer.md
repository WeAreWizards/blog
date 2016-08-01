Title: Why Docker is not the answer to reproducible research, and why Nix may be
Date: 2015-06-11
Short_summary: We look at how to do properly reproducible research, and why using Docker doesn't work.
Category: Infrastructure
Authors: Tom


In this post I'm going to assume that
[reproducibility](http://en.wikipedia.org/wiki/Reproducibility) is
good and necessary. There are
[well-written articles](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)
on how to do reproducible computational research so I don't want to go
into that either.

Instead I want to focus on how researchers can run published source
code on their own machines and arrive at the same results.
<!-- PELICAN_END_SUMMARY -->

## The issue with Docker

Unless you are publishing
[MIX assembly](http://en.wikipedia.org/wiki/MIX) all modern code comes
with a complex set of dependencies. Many of those dependencies - like
the GCC compiler - are invisible and taken for granted, but they are
still dependencies.

Recently I discovered people arguing for using
Docker for reproducibility (e.g. [here](http://www.nextflow.io/blog/2014/nextflow-meets-docker.html), [here](http://arxiv.org/abs/1410.0846) or [here](http://bioinfoblog.it/2015/03/reproducible-bioinformatics-pipelines-with-docker/)), and that is a scary idea. What follows is
a fairly common part of a `Dockerfile`, in this case for the
[Jupyter notebook](https://github.com/jupyter/notebook/blob/master/Dockerfile):

```
RUN apt-get update && apt-get install -y -q \
    build-essential \
    make \
    gcc \
    [...]
```

There are several issues here:

1. Running apt-get update means you will get whatever binary package
   is on the package mirror when *you* run the command.
2. While binary packages are signed you still don't know which
   libraries were installed on the system that built the package.

So the outcome of this `RUN` statement depends on:

* The time the command was run,
* the build environment of the package uploader,
* the base image in the Docker registry,
* and potentially on the package mirror used.

Now multiply this behaviour by many packages and their dependencies.

Reproducing your results even three years from now seems like an
unlikely proposition under those circumstances.

I don't think there are any *simple* solutions to this problem. Docker
looks superficially simple, and therefore tempting. However, I believe
using Docker (as it is used currently) for research would make things
genuinely worse. And I am
[not alone](http://ivory.idyll.org/blog/2014-containers.html) with
that opinion.


## A solution (maybe)

We need a package manager that encodes *all* dependencies for every
package in great detail, down to the bits of the source code. Flipping
a single bit in the source of the most basic package like GCC should
cause a dependency change for all packages that somehow rely on GCC,
both directly and indirectly.

This sounds complicated but someone found a way to make such a system
practical and published it under the name [Nix](https://nixos.org/).

In theory Nix allows re-compiling every binary on your system from
scratch and arriving at the same result. I have successfully rebuilt a
considerable amount of basic binaries like binutils and GCC.

NixOS achieves its tree-of-dependencies behaviour by encoding each
package as a function that depends on all its inputs. For example the
reasonably obscure [liblas](http://www.liblas.org) is encoded as
follows:

```nix
{ stdenv, fetchurl, boost, cmake, gdal, libgeotiff, libtiff, LASzip }:

stdenv.mkDerivation rec {
  name = "libLAS-1.8.0";

  src = fetchurl {
    url = "http://download.osgeo.org/liblas/${name}.tar.bz2";
    md5 = "599881281d45db4ce9adb2d75458391e";
  };

  buildInputs = [ boost cmake gdal libgeotiff libtiff LASzip];

  # ... Removed some metadata to avoid obscuring the point
}
```

Read that as a function taking parameters like the `boost`, `cmake`,
`gdal` and `libtiff` version. `stdenv` contains the usual Unix build
tools like GCC and a linker.

Crucially, the md5 hash is part of the input, and a change in hash
will result in a different version of this package. The same is true
for all its dependencies.


## In theory ...

In practice things are more complicated: Modern compilers are often
non-deterministic, especially when building in parallel. I.e. building
the exact same file twice does not necessarily result in the same
object code. Many distributions are spending considerable resources on
improving this situation and Nix
[is no exception](https://github.com/NixOS/nixpkgs/pull/2281).

Another source of variation is that linear algebra libraries like
OpenBLAS have specialised code for most CPU architectures, selecting
the fastest option at runtime.


## Summary

While Docker is tempting for shipping research I think it's the wrong
answer in its current incarnation. Between the systems that are usable
right now it looks like Nix gives us the best shot at
reproducibility. Nix still has a long way to go but it is build on a
sound foundation, not on shifting sands like current Docker.
