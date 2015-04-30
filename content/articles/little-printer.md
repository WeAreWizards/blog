Title: Berg's Little Printer
Date: 2015-04-30
Category: Misc
Authors: Tom
Short_summary: We did some pretty exciting work for Berg!

*Reading time: ~5 minutes.*

I'm a big fan of the amazing London design agency Berg. So when its
CEO Matt Berg tweeted this last year:

<blockquote class="twitter-tweet" lang="en"><p lang="en" dir="ltr">I&#39;m after a London Python freelancer for a 2mo gig, Flask/tests/Redis/Bootstrap. Mail me... matt at interconnected dot org. Tell yr friends!</p>&mdash; Matt Webb (@genmon) <a href="https://twitter.com/genmon/status/537304016993386497">November 25, 2014</a></blockquote> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

I was hooked.

<!-- PELICAN_END_SUMMARY -->

We emailed Matt and it turned out that he was looking for someone to
re-implement a server for their
[Little Printer](http://www.wired.co.uk/news/archive/2011-11/29/berg-little-printer-bergcloud).

The Little Printer is a thermal printer that can be controlled from
the Internet. The most popular use is sending little messages to your
Twitter friends. The proposition sounds a bit silly but after having
used it during development I can say that it is a fun item!

Along with the sad news that Berg was
[shutting down](http://blog.bergcloud.com/2014/09/09/week-483/) came
the good news that Matt wanted the Little Printer to live on. And the
best way to do so was to have a simpler server, divorced from the rest
of Berg's offerings.

By the time we arrived Matt had already implemented a few fairly
complicated parts for encoding the binary data sent to the Little
Printer. Despite that there were plenty of challenges left for us.


## Challenges

* All printers are constantly connected to the server, and need to
  react quickly to push notifications.
* The server should be easy to deploy: We needed to avoid complicated
  dependencies and interactions between moving parts.
* The protocol wasn't documented other than in the existing code base.


## Protocol implementation

We chose to go with a simple stratified design: We have a
socket-handling layer that deals with the online/offline status for
each printer. On top of that we have a message encoding and decoding
layer that translates the payload into Python's
[namedtuples](https://docs.python.org/2/library/collections.html#collections.namedtuple). The
last layer is a small website for user interactions.

<blockquote><h4>Aside</h4>Python's <code>namedtuple</code> is a useful
little tool that everyone should know. It creates a normal immutable
tuple, but unlike a normal tuple members can also be accessed by their
name. A quick example:

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">collections</span> <span class="kn">import</span> <span class="n">namedtuple</span>

<span class="n">User</span> <span class="o">=</span> <span class="n">namedtuple</span><span class="p">(</span><span class="s">&#39;User&#39;</span><span class="p">,</span> <span class="s">&#39;name email likes_cats&#39;</span><span class="p">)</span>

<span class="n">alice</span> <span class="o">=</span> <span class="n">User</span><span class="p">(</span><span class="s">&#39;Alice&#39;</span><span class="p">,</span> <span class="s">&#39;alice@example.org&#39;</span><span class="p">,</span> <span class="bp">True</span><span class="p">)</span>
<span class="n">bob</span> <span class="o">=</span> <span class="n">User</span><span class="p">(</span><span class="s">&#39;Bob&#39;</span><span class="p">,</span> <span class="s">&#39;bob@example.org&#39;</span><span class="p">,</span> <span class="bp">False</span><span class="p">)</span>
<span class="k">print</span><span class="p">(</span><span class="n">alice</span><span class="o">.</span><span class="n">name</span><span class="p">,</span> <span class="n">alice</span><span class="o">.</span><span class="n">email</span><span class="p">)</span>
<span class="k">print</span><span class="p">(</span><span class="n">bob</span><span class="p">)</span>
</pre></div>

Which outputs:

<div class="highlight">
<pre><code>Alice alice@example.org
User(name='Bob', email='bob@example.org', likes_cats=False)
</code></pre>
</div>

As you can see we can access the members defined for the
<code>User</code> class, and namedtuple also created a useful
<code>__repr__</code> for us.

</blockquote>

The stratified design made it easy to test and exchange individual
parts. E.g. we implemented a fake printer that runs on the command
line in very few lines of code.

The full flow is:

1. User action triggers creation of a `namedtuple` message
   (e.g. [print](https://github.com/genmon/sirius/blob/master/sirius/protocol/messages.py#L65))
2. [Encoding](https://github.com/genmon/sirius/blob/master/sirius/coding/encoders.py#L74) of the message.
3. [Sending message](https://github.com/genmon/sirius/blob/master/sirius/protocol/protocol_loop.py#L77) over socket to printer.


## Avoiding extra servers

To avoid an extra service for messaging we decided to keep
everything - protocol handling and web serving - in a single
process.

There are no printer-to-printer interactions. That makes sharding by
printer-ID trivial: We can stick with the single-process architecture
forever by just running more of the same.


## The human aspect

Working with Matt was a great experience. He is precise in his
communication and knows what he wants. Pretty much the ideal customer
for a small agency like ours!


## It's open source

You can find the code for the Little Printer [on Github](https://github.com/genmon/sirius).
