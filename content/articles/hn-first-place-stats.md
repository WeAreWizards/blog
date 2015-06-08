Title: The Hacker News effect and what we can learn from it
Date: 2015-06-08
Short_summary: Looking at the stats from being at the first spot on HN
Category: Misc
Authors: Vincent


*Reading time: ~10 minutes.*

Last week my article [Using Protobuf instead of JSON to communicate with a frontend](https://blog.wearewizards.io/using-protobuf-instead-of-json-to-communicate-with-a-frontend) ended up being number one on [Hacker News](https://news.ycombinator.com) and we saw a crazy amount of traffic coming on this blog. 

I thought that it would be interesting to analyze some of that data so here it is.
<!-- PELICAN_END_SUMMARY -->

## The data
It is coming from Google Analytics and while I could just paste screenshots, that wouldn't be any fun so I exported some of it as CSVs and used them in the notebook you can see below. The data is over the past month to have more insights on various social "strategies" (or rather, lack of) as you will see in a bit.  


{% notebook ga-stats.ipynb %}

## The server
Just a quick word to praise static sites: we ran 15 QPS excluding static assets (50 QPS including those) on a micro instance at 0.0 load with 500 concurrent users.  

We use [Pelican](http://docs.getpelican.com/en/3.5.0/) but any of the dozens of other similar tools is fine and you can handle ridiculous amount of traffic without any worries. You can also host the blog on S3 or a CDN if you don't want to have a server at all.  
Using a static site generator also makes it easy to review and improve articles, like you would do for code reviews. The only pain point is commenting on notebooks, as it is not possible to do so on the rendered version on Github and a notebook looks like [that](https://raw.githubusercontent.com/WeAreWizards/blog/master/content/notebooks/weather.ipynb).

You can check [our blog repo](https://github.com/WeAreWizards/blog) and look at the issues if you are curious about that process.

Now, onto vacations!
