Title: My experience of using NixOps as an Ansible user
Date: 2015-05-25
Short_summary: I reflect on my experience of having used Nix(OS/Ops) given my previous experience of Ansible
Category: Infrastructure
Authors: Gautier

*Reading time: ~15 minutes.*

One of our client recently asked us to host and support their existing Django
application.
Although my usual tools for this kind of jobs are Ubuntu and
[Ansible](http://www.ansible.com), I wanted to try the [Nix
tools](https://nixos.org/nix/) in a real project since Tom is an avid user.
<!-- PELICAN_END_SUMMARY -->

In this article I am writing about my experience of using NixOps to deploy
our client application on our infrastructure.

I am illustrating the practical differences between NixOps and Ansible using a
test project similar in terms of components to the application we deployed.

But first, let me introduce Nix and Ansible.

## Ansible

My favourite configuration management tool for the last couple of years has
been Ansible. It supports server configuration, server orchestration and
even resources provisioning (like an S3 bucket or a Google Compute Engine
instance) using the same simple language.

`ansible` is a tool to execute `modules` (i.e. to copy files, install packages,
start services) on remote servers listed in an `inventory` over `ssh`.

`ansible-playbook` uses YAML files to arrange the execution of `modules` in
`playbooks` making it a configuration management tool.

The YAML syntax is very readable, the execution model is straightforward and it
is easy to create new modules.
Also since Ansible doesn't need much more than SSH running or assume much about
the remote server it is easy to introduce into existing systems.

If you want to know more about Ansible, I recommend starting with the official
[How Ansible Works](http://www.ansible.com/how-ansible-works) article.

The reality of setting up a system, even with a configuration management tool,
is usually a trial and error process. The following is a typical example:

* Install database package
* Copy database configuration file
* Test database
* Fix anything wrong in the configuration and re-deploy
* Refactor the configuration
* Test it again
* Move on to the configuration of the web server

Using a tool like Ansible, this process exhibits a major flaw. If you were to
remove the line to install a package in an Ansible playbook, the package would
still be installed on the server you are configuring. Which means that after a
refactoring phase the server will work properly but with an incomplete
configuration. This problem is not limited to packages, but also to the
presence of users, files, their permissions, their content... Anything you
could configure with Ansible.

The result of this flaw is that even if you managed to get a server properly
configured once, you don't know if it will work again.
If you change your server configuration over time without creating new
servers, then you need to make sure your configuration files does not diverge
from the actual state of the server.

Also, even if you tested your playbooks well, it is still possible for them to
stop working if a system package or application dependencies has been updated
in your system.

## Nix

This is where the Nix project comes in. It consists of [Nix, The Purely
Functional Package Manager](https://nixos.org/nix/), [NixOS, The Purely
Functional Linux Distribution](https://nixos.org/) and [NixOps, The NixOS Cloud
Deployment Tool](https://nixos.org/nixops/).

Nix produces packages that link to all their dependencies at specific versions
and that are entirely independent from each other.

NixOS is a simple and modern Linux distribution configured declaratively using
the same language as Nix packages.

Finally, NixOps is used to configure a «network» of NixOS systems, still using
the same language.

The learning curve for those tools is steep, the official documentation is
light and there aren't that many resources available on the web about Nix so I
had to learn it mostly by reading the source of the tools. Also, NixOps being a
young project I hit a few open bugs.

The [Nix manual](https://nixos.org/nix/manual/) is a good start to learn about
the package manager. This [Nix by example
article](https://medium.com/@MrJamesFisher/nix-by-example-a0063a1a4c55)
describes the Nix expression language in more detail.
To understand the rationale behind Nix and NixOS, you can read the accessible
[NixOS: A Purely Functional Linux
Distribution paper](http://nixos.org/~eelco/pubs/nixos-jfp-final.pdf).

For more practical questions, I found that the best way to learn was to find a
package that resembles what I wanted to do and get inspiration from its
corresponding expression. NixOS packages can be found using the [Search NixOS
packages page](https://nixos.org/nixos/packages.html).


## Comparing the deployment of a test application

Using the [test
project](https://github.com/WeAreWizards/voting-deployment-test), I am going to
illustrate the practical differences between using NixOps and Ansible.

### Dependencies

Nix is first and foremost a package manager, so the most common way to deploy
applications is to build packages locally and copy them to servers.

Nix being `purely functional`, it should build the same output (a closure)
given the same input (an expression). To do so, Nix needs all dependencies
retrieved at build time.

Assuming the dependencies you need are present in the nixos channel and at the
right version, you can just refer to them as in the `default.nix` file of the
test project:

```nix
pythonPackages.buildPythonPackage {
    name = "voting";

    propagatedBuildInputs = [
        pkgs.python27Packages.django
        pkgs.python27Packages.sqlite3
        pkgs.python27Packages.gunicorn
    ];

    src = ./.;
}
```

However, if your dependencies are not in the nixos channel, you will need to
declare them manually.

For example the requests python library is declared like this:

```nix
requests = buildPythonPackage rec {
  name = "requests-1.2.3";

  src = pkgs.fetchurl {
    url = "http://pypi.python.org/packages/source/r/requests/${name}.tar.gz";
    md5 = "adbd3f18445f7fe5e77f65c502e264fb";
  };

  meta = {
    description = "An Apache2 licensed HTTP library, written in Python, for human beings";
    homepage = http://docs.python-requests.org/en/latest/;
  };
};
```

Which means than when building the package you are still dependent on pypi
being up, unless the package is already cached.
You can notice that the checksum of the archive is checked, so Nix will
only build if the source package hasn't changed.

Compared to a `requirements.txt` file, this is clearly more work. Fortunately
the pypi2nix can take a `requirements.txt` file and write the corresponding
derivations.

Ansible doesn't have a single way of the handling of application dependencies.
A common technique for a Python application is to install system packages with
the distribution packages and python dependencies through pip.

In the case of the voting test project this looks like this:

```yaml
    - name: global packages
      apt: name={{item}} state=installed
      with_items:
        - python-virtualenv
        - git
        - uwsgi
        - uwsgi-plugin-python
        - nginx
      sudo: yes

    - name: python dependencies
      pip: name=django version=1.6.6
      sudo: yes
```

Of course, nothing stops you from building distribution packages locally and
sending them to your servers with Ansible.

### Provisioning

The general principle around provisioning is to ask for a set of servers to be
running on which to deploy the application. A configuration management
provisioning tool should start server that are not already running and re-use
the ones that are.

To keep track of the resources created by a deployment configuration, NixOps
stores their name, state and access keys in a `state` file.
Then when deploying, NixOps first matches the resources instantiated in the
cloud provider to the state file and applies the changes needed to be in the
state declared by the configuration.

><h4>TIP</h4>Don't include the test server and the production server
of a project in the same state file.

NixOps doesn't provide a way to share this state file across machines so the
currently best solution is to [deploy from a shared
machine](http://lists.science.uu.nl/pipermail/nix-dev/2015-February/016322.html).
This is the main difficutly we encountered with NixOps as a shared machine is a
single point of failure in terms of availability and security. Also, this
forces us to somehow first deploy the shared deploy machine and then the other
servers from there.

On the other hand, most Ansible modules don't store the state of the deployment
locally.

When using Ansible I've often seen the provisioning handled outside of the
playbooks and when it is done with Ansible, the provisioning is in a separated
role and the servers set up at fixed DNS names which then the application
deployment roles connect to.

In the voting test project I have shown how it is possible to provision servers
and configure applications in the same playbook with Ansible.

### Speed

It takes about 3 minutes for both NixOps and Ansible to deploy the test
project from scratch.

For a deployment with no change, it takes about 12 seconds with Nix and 17 with
Ansible.

Of course this is entirely anecdotal, so don't read too much into these
numbers.

As much as NixOps being a bit faster than Ansible matches our experience, this
is not something fundamental. It is possible to make Ansible deploy
applications quickly.
Also, where Ansible has `ansible-pull` to handle large scale deployments,
NixOps could be problematic as the closures have to be copied over the network
to each servers.

### Services configuration

Based on the same language as the Nix expressions, NixOS introduces the
`module` abstraction. Modules are used to configure an entire system including
UNIX users, systemd units or services like Apache and Postfix.
This makes it possible to configure the full state of the system in a single
top-level module. The `voting-server` attribute is in the `voting.nix` file of
the test project is an example of a NixOS system configured using modules.

You can see how the nginx module is used:

```nix
      services.nginx.enable = true;
      services.nginx.config = ''
  events { }
  http {
    include ${pkgs.nginx}/conf/mime.types;

    server {
      listen 80 default_server;
      server_name _;

      location /static/ {
          alias ${app}/lib/python2.7/site-packages/voting/static/;
      }

      location / {
        proxy_pass http://localhost:8000;
      }
    }
  }
  '';
```

With Ansible, some modules manage part of the system like UNIX users, but the
configuration of most services is managed at the file level: configuration
files are copied to a specific location and the service restarted.

For example, this is how nginx is configured in the test project:

```yaml
    - template:
        src=files/voting.conf.j2
        dest=/etc/nginx/sites-enabled/default
        owner=root
      sudo: yes
      notify: restart nginx
```


### Rollback

Sometimes a deployment goes wrong and the best way forward is to take a step
back.

When doing an upgrade, NixOS sends the new closures, containing packages and
configuration, and then atomically change the whole system by changing one
symlink without overwriting the previous versions of the closures.

This means that NixOps has the ability to revert a deployment atomically,
quickly and safely in a single command.

<blockquote><h4>Note</h4>Nix(OS) doesn't manage mutable state. If your
application has migrated the schema of a database, Nix will not undo the
migration for you!</blockquote>

Ansible on the other hand doesn't deal with rollbacks.

## Conclusion

My opinion is that Nix and NixOS are not only fascinating but the *right*
way of packaging applications and configuring systems.

The positive side of knowing Nix comes at an ironic cost: realising issues that
should not happen any more when using other systems!
For example, how often have I seen problems related to dependencies at the
wrong version, either on my end when I can't get something working or when I
can't reproduce the problem of someone else?

However, the Nix projects require quite a jump in terms of learning and the
NixOps state file has caused us trouble.
This is why we are not yet commited to using NixOps exclusively. We will keep
investigating other solutions and report on this blog with updates!
