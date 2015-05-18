Title: Comparing the weather of places I've lived in
Date: 2015-05-18
Short_summary: Using python to compare weather data in 4 places
Category: Dev
Authors: Vincent

*Reading time: ~25 minutes.*

I have lived in 4 countries on 3 continents (so far).  
When people ask me about these places, the first thing that comes to my mind is the weather.
Having lived in these places I knew roughly how they compared but was curious about the exact numbers. What better way than to visualize data than a ipython notebook!
<!-- PELICAN_END_SUMMARY --> 

We're going to look at the following four places:

- Nice, France (my hometown)
- London, England
- Montreal, Canada
- Naha, Japan: in Okinawa, see [Google Maps](https://goo.gl/maps/s520D) for exact location

> I lived in Uruma, not in Naha but Naha being the capital city of Okinawa, the data is coming from there. Okinawa is not really big though so it's ok to use that data.

## Getting the data
There are weather stations all over the world but finding their data can be a bit tricky. Also, Nice is a very hard term to google surprisingly enough.  
I managed to find data for all the cities but Nice on various local websites when Tom linked [TuTiempo.net](http://en.tutiempo.net/climate) which aggregates that data in a single place. Great, only one website to scrape!  
The [script](https://gist.github.com/Keats/0ba9be4e514b2a90e59f) is quite simple and only depends on [requests](https://pypi.python.org/pypi/requests) and [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4). You can run it if you want but there are some limitations like requiring folders to exist or having to delete the CSV before running it again. 
The four CSV and the following notebook are available on this [repo](https://github.com/Keats/cities-article).

## Looking at the data
You can see the notebook below.

{% notebook weather.ipynb %}
