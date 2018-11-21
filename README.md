# ccbot [![travis build for ccbut](https://api.travis-ci.org/hattan/ccbot.svg?branch=master)](https://travis-ci.org/hattan/ccbot)

SoCal Code Camp Slack bot - https://www.socalcodecamp.com/

## Installation

In order to use ccbot with slack, you need to create a [slack app](https://api.slack.com/apps?new_app=1). After creating an app, you need to get you API Token. That token needs to be added to an environment variable named 'SLACK_CODE_CAMP_BOT_TOKEN'

Install deps : 

    `pip install -r requirements.text` 

Start bot:

    `ccbot/bot`

The bot should be up and running.

Note: If you would like the bot to work in private channels, you need to invite the bot to the channel.

## Unit Tests

Run tests (from root of the project):

    `pytest` 

To run tests continuously via [pytest-watch](https://github.com/joeyespo/pytest-watch):

    `ptw`

### Code Coverage

    `./cover.sh`

## Adding new Commands

Commands are automaticatlly loaded at startup. To add a new command, add a class in the commands folder. The class must include
the following 3 method:

| Method | Description |
|---    |---    |
|`get_channel_id(self)`|Returns the channel ID where this command can execute. It can also be "all" for any public or private channels which have ccbot as a member.|
|`invoke(self, command, user)`| This method gets called everytime someone invokes the command. The `command` parameter contains the name of the command, and any other trailing arguments as a single string.|
|`get_command(self)`|Text used to invoke command. The input can contain other characters after the command text.|

## Current Command List

* `campme` &lt;verb&gt; - shows current code camp sessions and schedule. Try `campme now` for sessions in progress, `campme next` for sessions about to start, `campme speaker Bob Bobbernaugh` for session by Bob Bobbernaugh, `campme sessions at 14:15` to show sessions _today_ at 2:15PM (use 24 hour clock, hour and minutes only).
* `catme` - shows a catgif from [Edgecats](http://edgecats.net/)
* `dogme` - shows an image of a puppy
* `goatme` - shows an image of a goat
* `tortoiseme` - shows an image of a tortoise
* aww - shows an image from [/r/aww](https://www.reddit.com/r/aww/)
* `teslame` - shows an image of an [intergallatic spaceboat of light and wonder](http://theoatmeal.com/comics/tesla_model_s). Note: It's TeslaME not tesLAME.
* `earthme` - shows an image of the earth.
* `xkcd` - shows a random xkcd comic
  * `xkcd latest` - shows the most recent xkcd comic
  * `xkcd [number]` - shows an xkcd comic by it's id. eg "xkcd 221" (which is one of my favorites)
* `tacome` [zip code] - shows a random yelp business categorized 'tacotrucks' with term 'taco'
* `ccbot` - generic ccbot command. ccbot must be invoked with a command in the form ccbot [command]. Commands are mapped to functions that start with "action_"
  * ccbot tell_joke - grabs a dad joke and displays the text
* `whome` - shows an image related to __Dr. Who__.
* `AlfMe` - A random __Alf__ GIF.
* `BobMe` - A random __Spongebob Squarepants__ GIF.
* `ElfMe` - A random __Elf__ GIF.
* `HanukkahMe` - A random __Hanukkah__ GIF.
* `KillMe` - A random __Kill Bill__ GIF.
* `KwanzaaMe` - A random __Kwanzaa__ GIF.
* `MadMaxMe` - A random __Mad Max__ GIF.
* `MarxMe` - A random __Groucho Marx__ GIF.
* `StaloneMe` - A random __Silvester Stalone__ GIF.
* `StarTrekMe` - A random __StarTrek__ GIF.
* `StoogeMe` - A random __Three Stooges__ GIF.
* `UrkleMe` - A random __Steve Urkle__ GIF.
* `HelpMe` - Shows available commands. 
  * `HelpMe [command]` - More details about an individual command options (if documented). Try `helpme urkleme`


![Image of ccbot invoking earthme and xkcd](https://i.imgur.com/Pol1L0l.png)
