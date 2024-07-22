

Grabs weather data from FMI service and toots it to Mastodon.



Requires

* python 3.11.9+


```
pip install owslib python-dotenv fmiopendata
```



Thanks for data

* https://en.ilmatieteenlaitos.fi/open-data-manual



### TODO

* add emojis to toot for weather flare
* datetime utc warning deprecation removal on 3.12
* Bug: in some cases multiplace use skips a place(?) (give 3, get 2)


### Done

* Redone with  https://github.com/pnuu/fmiopendata 
* added rain & snow info
* nicer formatting for datestamp -> (at least is local time accurate)
* * Show data for bit more places for efficiency 4x4? -> can give names via , -list.


* 🐈‍⬛