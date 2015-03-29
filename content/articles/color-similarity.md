Title: How to build a simple image/primary-colour similarity database
Date: 2014-12-23
Short_summary: We describe a simple colour-similarity search algorithm using clustering and nearest-neighbour search.
Category: Misc
Authors: Tom

We recently talked to some customers who are interested in finding images with similar colours in the context of fashion. There are several known solutions for this, and even some hosted services that do it for you.
<!-- PELICAN_END_SUMMARY -->

Our case is a little bit different though because the images in the
database change frequently. That rules out a fully supervised learning
system due to the high cost of labelling new images all the time.

Anyway, here's a small IPython notebook that explains the approach we
chose. Note that this is only a *very simple* prototype that delivers
a bad to OK experience. A fully tuned system takes advantage of
training the ranker with click-stream data, uses a more human-friendly
colour-space etc.

{% notebook color-similarity.ipynb %}
