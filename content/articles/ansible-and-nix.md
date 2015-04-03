Title: My experience with Nix as an Ansible user
Date: 2015-04-03
Short_summary: I reflect on my experiences of using Ansible and Nix to deploy applications 
Category: Infrastructure
Authors: Gautier


We recently deployed a Django application using a less known linux distribution:
[NixOS](https://nixos.org/).

In this article I'm writing about my experience of configuring a new server
with Nix given my previous experience with Ansible. I'm not getting into much
details into either [Ansible](http://docs.ansible.com/) or
[Nix](https://nixos.org/) and focus mostly on my experience.

## Ansible

My favourite configuration management tool for the last couple of years has
been Ansible. It supports server configuration, server orchestration and
even resources provisioning (like an S3 bucket or a Google Compute Engine
instance) using the same simple language.

Its yaml syntax is clear, its execution model is straightforward and it is easy
to extend.

The reality of setting up a server or a set of servers with a configuration
management system is a trial and error process:

* Configure the database
* Test database
* Fix anything wrong
* Refactor the configuration
* Test it again
* Move on the web server

Using a tool like Ansible this process has a major flaw .  If you were to
remove the line to install a package in an Ansible playbook the package would
still be installed on the server you are configuring. Which means that after a
refactoring phase the server might work properly but with an incomplete
configuration is incomplete.  This problem is not limited to packages, but also
to the presence of files, their permissions, their content... Anything you can
configure with Ansible.

The result of this flaw is that even if you managed to get a server properly
configured once, you are not finished yet and need to re-install from scratch
to make sure it actually works. However, if you change your server
configuration over time without creating new server, then you need to make sure
your configuration files does not diverge from the actual state of the server.

## Nix

This is where the Nix project comes in.  It consists of Nix, The Purely
Functional Package Manager, NixOS, The Purely Functional Linux Distribution and
NixOps, The NixOS Cloud Deployment Tool.

Nix produces packages that contain all their dependencies and that are entirely
independent from each others.  The result from these properties means that you
cannot get into the problem illustrated previously.

NixOS is a simple and modern Linux distribution configured declaratively using
the same language as Nix packages.

Finally, NixOps is used to create deployments on NixOS systems.

The learning curve for those tools is steep, the official documentation light
and there arent't many resources available on the web about Nix so I had to
learn it mostly by reading the source of the tools. Also, NixOps being a young
project I hit a few open bugs.

The main difficulty we encountered with NixOps is sharing the NixOps state file
which is a sqlite database containing passwords, ssh keys, EC2 instance IDs.
NixOps doesn't provide a way to share this file across machines so the best
currently accepted solution is to [deploy from a shared
machine](http://lists.science.uu.nl/pipermail/nix-dev/2015-February/016322.html).

My opinion is that the Nix projects are fascinating and sound like the *right*
way of packaging applications, deploying them and configuring systems.

One annoying thing about having used Nix is that I now notice problems that
shouldn't happen any-more. The classic «it works for me» when it doesn't for
someone else and finding out the exact version of library causing the issue
wastes a lot of time.

## Conclusion

I'm amazed by how effective the Nix basic ideas are and how the team managed to
build an entirely new but usable and useful Linux distribution.

But as much as Nix solves a major flaw of classic configuration management
tools, it comes with its own set of problems.

In the mean-time I think I'm going to keep using Ansible but maybe will use
Immutable Servers to solve the issue of keeping the written configuration in
sync with the actual state of the servers.
