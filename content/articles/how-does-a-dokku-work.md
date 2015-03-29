Title: How does a Dokku work?
Date: 2015-01-19
Short_summary: We explore how Dokku makes data from your Git repository appear as a web service.
Category: Infra
Authors: Tom

*Reading time: ~15 minutes.*

There are many implementations for running code in a way pioneered by Heroku which is basically this:
<!-- PELICAN_END_SUMMARY -->

1. Push a web service, let's call it **catmeow**, to a remote git repository.
2. The remote side "checks out" the git repository locally (on the server).
3. The remote side runs some framework-specific init code.
4. The remote side runs the server.

The catmeow service is generally configured through environment
variables, writes logs to `stdout` and follows most of the points in
[12factor.net](http://12factor.net/).

There is a very simple yet woking implementation of this model called
[dokku](http://progrium.viewdocs.io/dokku/index) which we're going to
investigate instead of Heroku. Dokku is not as powerful as Heroku,
missing e.g. auto-scaling, but it is Free Software and super
understandable.

Here we look at how your local git commit is transformed to a running
web service.

## The catmeow local git repository

This isn't a
[Heroku tutorial](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
but let's assume you have the following on your laptop:

```console
$ ls
catmeow.py  requirements.txt  Procfile
$ cat requirements.txt
flask
$ cat Procfile
web: python catmeow.py
```

`catmeow.py` looks like this:

```python
import os, flask

app = flask.Flask(__name__)
@app.route('/')
def catmeow():
    return "Cat dreams meow.."

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

We can now create a git repository and push to our Dokku instance
(for this demo we picked the standard digital-ocean one):

```console
tom@laptop$ git add requirements.txt Procfile catmeow.py
tom@laptop$ git commit -m"Do cats dream of meow?"
```

So far we have been very standard. Now we're going to push our remote
Dokku instance. Pushing triggers a fair amount of output which we'll
work through in the remainder of this post.

## The push

Git uses ssh behind the scenes. Superficially a push looks like this:

```console
tom@laptop$ git remote add dokku dokku@104.236.81.129:catmeow
tom@laptop$ git push --set-upstream dokku master
Counting objects: 5, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (5/5), 486 bytes | 0 bytes/s, done.
Total 5 (delta 0), reused 0 (delta 0)
```

If git is using ssh then why can't you login to Heroku or Dokku with ssh?
The answer can be found in the server's `.ssh/authorized_keys` file:

```console
root@remote:/home/dokku# cat .ssh/authorized_keys
command="FINGERPRINT=c8:a7:a6:67:ed:29:c4:a0:fe:fa:46:0d:79:1a:81:00
         NAME=admin `cat /home/dokku/.sshcommand`
         $SSH_ORIGINAL_COMMAND",
no-agent-forwarding,
no-user-rc,
no-X11-forwarding,
no-port-forwarding ssh-rsa AAAAB3NzaC1[...]
```

Note the `command`, `no-user-rc` etc. parts before the actual ssh-rsa key? ssh
allows specifying a bunch of options for each authorized key. All of
the options above are necessary for a reasonably secure setup but
the real magic happens in `command`.

`command` exports a few environment variables and then calls the content of `/home/dokku/.sshcommand`:

```console
root@remote:/home/dokku# cat .sshcommand
/usr/local/bin/dokku
```

Aha! Whenever git logs in with ssh it doesn't talk to another git
command; it talks to Dokku. How does Dokku know what to do when git
talks to it? Looking at
[the code](https://github.com/progrium/dokku/blob/v0.3.13/plugins/git/commands)
we see it's a little bit involved:

1. If Dokku is called with `git-receive-pack` (i.e. from a git push)
   for the first time then it installs a pre-receive-hook.
2. Dokku then invokes `git-shell` with all the original arguments, thus
   running the normal git push flow.
3. The pre-receive hook is called after git has received all
   data. The hook is a shell script which calls `dokku git-hook`.
4. `dokku git-hook` clones the current master into a temporary
   directory and then *finally* calls `dokku receive`.

Phew.

The last bit I described looks like this:

```console
-----> Cleaning up ...
remote: Cloning into '/tmp/tmp.3Au5pwF45H'...
-----> Building catmeow ...
remote: warning: You appear to have cloned an empty repository.
remote: done.
remote: HEAD is now at 05902bc... Do cats dream of meow?
-----> Cleaning up ...
remote: Cloning into '/tmp/tmp.3Au5pwF45H'...
-----> Building catmeow ...
remote: warning: You appear to have cloned an empty repository.
remote: done.
remote: HEAD is now at 05902bc... Do cats dream of meow?
```

There are clearly a lot of moving parts before Dokku can use the
catmeow commit we just pushed.


## The dokku receive story

The remaining steps are fairly straight forward. Dokku has cloned the
repository so it has an actual directory with your code in it. We see:

```console
-----> Python app detected
```

This output comes from a separate package called
[buildstep](https://github.com/progrium/buildstep/blob/2014-12-16/builder/compile.sh#L64). The
build step runs in a docker container, hence the name Dokku. The rest
is just standard Heroku build pack action. Installing some pip etc.:

```console
-----> Stack changed, re-installing runtime
-----> Installing runtime (python-2.7.8)
-----> Installing dependencies with pip
       Downloading/unpacking flask (from -r requirements.txt (line 1))
       Running setup.py (path:/tmp/pip_build_u21387/flask/setup.py) egg_info for package flask
       [------------✂------------✂------------✂----]
       [ snipping out a lot of irrelevant output.. ]
       [------------✂------------✂------------✂----]

-----> Discovering process types
       Procfile declares types -> web
-----> Releasing catmeow ...
-----> Deploying catmeow ...
=====> Application deployed:
       http://catmeow.remote

To dokku@104.236.81.129:catmeow
 * [new branch]      master -> master
```

One last interesting note is that Dokku has an interesting plugin
system that allows e.g. reconfiguring nginx after a push or creating
PostgreSQL containers so it's not just a toy.
