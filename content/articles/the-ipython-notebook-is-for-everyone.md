Title: The IPython notebook is for everyone
Date: 2014-09-27 10:20
Category: python
Author: Gautier Hayoun
Status: draft

This post is the adaptation of the presentation I gave at PyCon UK 2014.
In this article I'd like to show what is IPython, what it is good for and why I
think everyone should give it a try.
<!-- PELICAN_END_SUMMARY -->

## What is IPython?

IPython is already known from most Python developers as this Python interpreter
more advanced than the one included with Python.

In terms of features IPython can do tab completion :
```python
In [1]: text = "HELLO WORLD"

In [2]: tetris = 2

In [3]: te<TAB>
tetris  text
```
Or explore attributes of objects :
```python
In [1]: d = {}

In [2]: d.i
d.items       d.iteritems   d.iterkeys    d.itervalues
```

Conveniently display documentation of functions :
```python
In [1]: d = {}

In [2]: d.items?
Type:        builtin_function_or_method
String form: <built-in method items of dict object at 0x7f30eb92d050>
Docstring:   D.items() -> list of D's (key, value) pairs, as 2-tuples
```
And even execute shell commands straight from the interpreter :

```python
In [1]: cd /
/

In [2]: ls
bin/    etc/             lib/     lost+found/  proc/  srv/  var/
boot/   home/            lib32/   media/       root/  sys/  vmlinuz@
cdrom/  initrd.img@      lib64/   mnt/         run/   tmp/  vmlinuz.old@
dev/    initrd.img.old@  libx32/  opt/         sbin/  usr/
```

Those features make IPython a good tool to improve productivity.

## The IPython architecture

However I believe the greatest thing about the IPython project is its
high-level architecture.
The execution of code has been encapsulated into the kernel and the user
interaction into the front-end. The kernel and front-end communicate between
each other using ZeroMQ which means the front-end doesn't even have to be on
the same machine as the kernel.

Side note : *Oh, by the way the kernel doesn't have to execute only Python
code, nothing stops you from using the IPython notebook with various other
languages like R or ruby if you so fancy!*

This is how I picture this (it somehow looks a lot prettier in my head):

![IPython architecture]({filename}/images/ipython/kernel.png)

The IPython developers used this architecture to create various interesting
front-ends, including the IPython notebook but I'm going to mention some of the
others here.

The terminal based interactive IPython interpreter is the commonly used one,
the IPython Qt Console which features mostly the same terminal based
interactive Python interpreter but adds support for inline plots, images and
multiline editing.

## What is the IPython notebook?

According to the IPython website, it is :

> A browser-based notebook with support for code, text, mathematical
> expressions, inline plots and other rich media.

It is a notebook similar to a regular paper-based notebook.

![notebook]({filename}/images/ipython/notebook.jpg)
