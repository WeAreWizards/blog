Title: Launching Passopolis, a password manager
Date: 2015-08-18
Short_summary: Mitro, our favourite password manager is shutting down. We took over.
Category: Product
Authors: Vincent


I am assuming most readers of this blog know the benefits of password manager and how everyone should use one but for the few that don't: they generate random, unique password and remember them for you, protecting you from leaks from poorly run websites such as the ones on [Plain Text Offenders](http://plaintextoffenders.com/) and just generally increasing security.
<!-- PELICAN_END_SUMMARY -->


There are a few options when it comes to products in that space:

- [LastPass](https://lastpass.com/)
- [1Password](https://agilebits.com/onepassword)
- [Keepass](http://keepass.info/)


While all of us were already using one of these, we then had the need to share passwords or information with the team securely.


We initially tried LastPass for that but were not convinced. Tom found a greate alternative called [Mitro](https://www.mitro.co/) which was on maintenance mode at the time and now announced they are shutting down on September 30th. Thankfully they shared the sourcecode on [github](https://github.com/mitro-co/mitro), allowing us to run it ourselves. Many people were in the same situation as can be seen in this [issue](https://github.com/mitro-co/mitro/issues/123).


We spent a couple of days fixing some bugs and making it run on NixOS. It is available at [passopolis.com](https://passopolis.com) and free for anyone to use for now, though we may charge a small amount for teams later on but nothing is decided on that front yet.
Note that the design of the website is intentionally basic as we just wanted the servers and extensions to work really.


Of course, if you prefer running it on your own servers, you can use our repos for the [server](https://github.com/WeAreWizards/passopolis-server) and the [extentions](https://github.com/WeAreWizards/passopolis-extensions).
If you look at the issue linked above, some people are working on a Docker setup if that's your preference.


So here you go, if you are not using a password manager I recommend that you use one of those listed above or run your own!
