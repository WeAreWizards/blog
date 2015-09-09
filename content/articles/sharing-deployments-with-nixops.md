Title: How to use NixOps in a team
Date: 2015-09-09
Short_summary: NixOps is a great tool for running nix-based servers. We show how to do that in a team.
Category: Dev
Authors: Tom

[NixOps](https://github.com/NixOS/nixops) is a fantastic tool for
getting reproducible servers running in no time. NixOps can deploy to
many different targets including VirtualBox, Google's GCE and Amazon's
cloud services AWS.

[As we have discovered](https://blog.wearewizards.io/my-experience-of-using-nixops-as-an-ansible-user)
NixOps has the downside of storing all its state (such as the IP
address of a server) in a binary SQLite database. That in combination
with some defaults such as absolute paths make it a bit cumbersome to
share deployments. This post describes how to work around these
issues.

<!-- PELICAN_END_SUMMARY -->

## Defining a server

We'll define an extremely simple server that doesn't do anything other
than warming this planet:

```nix
# network.nix
let
    region = "eu-west-1";
in rec {
    network.description = "test-network";
    resources.ec2KeyPairs.test-keys = { inherit region; };

    server = { resources, pkgs, lib, ... }: {
        deployment.targetEnv = "ec2";
        deployment.ec2.region = region;
        deployment.ec2.instanceType = "t1.micro";
        deployment.ec2.spotInstancePrice = 7;
        deployment.ec2.keyPair = resources.ec2KeyPairs.test-keys;
    };
}
```


### Trick 1 and 2: Confining NixOps to a single directory

Our first two tricks are to circumvent the default NixOps-behaviour of
using absolute paths (by using angular brackets `<...>`), and to store
the state for our deployment in a local file (by using `-s ...`):

```
$ NIX_PATH=${NIX_PATH}:. nixops create -s localstate.nixops -d test '<network.nix>'
created deployment ‘1b699a42-5709-11e5-ad66-542696dce997’
1b699a42-5709-11e5-ad66-542696dce997
```

The angular brackets `<...>` tell the nix command to search for
`network.nix` in the `NIX_PATH`. And we just set `NIX_PATH` to point
to the current directory.

Using a local state file (`-s localstate.nix`) means we can check the
state into git (more on that later).


### Trick 3: Using direnv to simplify

That's a lot of environment variables and parameters to type. In order
to clean up the command invocation we're using a wonderful tool called
[direnv](https://github.com/direnv/direnv) which exports environment
variables from a `.envrc` file when entering a directory.

An `.envrc` for AWS deployment typically looks like this:

```bash
export AWS_ACCESS_KEY_ID="AKIA...."
export AWS_SECRET_ACCESS_KEY="eexie9Ieeel9XieCThish5..."
export NIX_PATH=${NIX_PATH}:.
export NIXOPS_STATE=localstate.nixops
```

We can now inspect the test network we just created with `nixops
info`:

```console
$ nixops info
Network name: test
Network UUID: f29084f8-570c-11e5-83af-542696dce997
Network description: test-network
Nix expressions: <network.nix>

[...]
```

And deploy:

```console
$ nixops deploy
test-keys> uploading EC2 key pair ‘charon-f29084f8-570c-11e5-83af-542696dce997-test-keys’...
server...> creating EC2 instance (AMI ‘ami-0126a576’, type ‘t1.micro’, region ‘eu-west-1’)...
server...> waiting for spot instance request ‘sir-01pq1vda’ to be fulfilled... [pending-evaluation] [fulfilled]
server...> cancelling spot instance request ‘sir-01pq1vda’... [request-canceled-and-instance-running]
server...> waiting for IP address... [pending] [running] 54.76.8.50 / 172.31.30.116
server...> waiting for SSH......
```


### Trick 4: Sharing secrets in git

Keeping AWS keys or any secrets in git unencrypted is a recipe for
disaster. Bitcoin miners constantly scan Github for accidental AWS key
uploads and will have spent thousands of your $CURRENCY before you can
blink. The NixOps state file itself contains SSH root keys, exposing
those keys is the same as having the machine owned with a zero day
exploit.

**Keeping either the statefile or the `.envrc` with your AWS keys
in git unencrypted is grossly negligent.** I know this is common
knowledge but I prefer to over-communicate on this issue.

We're using a tool called
[git-crypt](https://github.com/AGWA/git-crypt) to securely share
secrets in a git repository. git-crypt creatively uses the
`.gitattribute` file to encrypt certain files in the repository.

First we initialize git-crypt:

```console
$ git-crypt init
Generating key...
$ git-crypt status
not encrypted: .envrc
not encrypted: localstate.nixops
not encrypted: network.nix
```

Now we set up the `.gitattributes` file:

```console
$ cat .gitattributes
localstate.nixops filter=git-crypt
.envrc filter=git-crypt diff=git-crypt
```

Double-check the encryption works:

```console
$ git-crypt status
    encrypted: .envrc
not encrypted: .gitattributes
    encrypted: localstate.nixops *** WARNING: diff=git-crypt attribute not set ***
not encrypted: network.nix
```

Note that we didn't set `diff=git-crypt` on `localstate.nixops`
because it is a binary SQLite file.


### A safer .gitattributes

Keeping encrypted files in many different places in the repository can
cause accidental exposure due to human mistakes so we generally have a
`secrets` directory for all the secret things (except for `.envrc`
which needs to stay top-level).

For example:

```console
$ cat .gitattributes
secrets/* filter=git-crypt
.envrc filter=git-crypt diff=git-crypt
```

### Pinning a specific NixOS release

As of Nix 1.9 one can refer to a specific release using HTTP, so we
tend to pin our relase like so in the `.envrc` file to make sure that
everyone with the repository references the same set of nix packages:

```shell
# .envrc
export NIX_PATH=nixpkgs=https://github.com/NixOS/nixpkgs-channels/archive/nixos-15.09.tar.gz:.
```


### Downsides of this scheme

* Many commands like `deploy`, `backup`, etc modify the state file,
requiring either a commit or the conscious choice to blast away state
file changes with `git checkout -f` if you are sure it's safe to do
so.

* The SQLite format isn't easy to diff. I'm sure we could improve the
diff using e.g. [sqldiff](https://www.sqlite.org/sqldiff.html) but I
think I'd prefer a text format based on e.g. protocol buffers or JSON.


# This works well

This bag of tricks might look a bit complicated but works very well
for us in practice.
