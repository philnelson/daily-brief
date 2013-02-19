daily-brief
===========

A python script that generates a daily briefing email ideal for having Siri or OS X's 
speech tools read back to you.

Installation
------------

I always recommend using virtualenv and virtualenvwrapper and so I've only done the 
following inside a virtualenv.

1. `pip install -r requirements.txt` (installs feedparser, nltk and their dependencies.)
2. run `./brief.py --nltk-first-run` to install the necessary nltk corpora and tokenizers
(used for the summarization feature)
3. create a file called brief.config that will hold the configuration values in a 
JSON format.

Configuration (brief.config)
----------------------------

Here's a sample of what the contents should look like:

<pre>
{
	"name": "Sir",
	"from": "your@email.com",
	"to": "your@email.com",
	"feeds": {
		"headlines": "http://www.npr.org/rss/rss.php?id=1001",
		"weather": "http://w1.weather.gov/xml/current_obs/KBFI.rss"
	},
	"smtp": {
		"host": "localhost"		
	}
}
</pre>

(It should be noted that the script is over-optimized for weather.gov and npr.org feeds.)

Running
-------

If you'd like to see what the output will look like or want to pipe the output somewhere 
else use the `--to-text` flag.

Presumbly you'll want to have a cron job send this every morning:

`0 7 * * * the/path/to/brief.py`

That's really it for now. There should probably be more options and such.