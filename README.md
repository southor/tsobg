
# T.S. Online Board Game

## Description

Project under development, it is a platform for testing new boardgame prototypes in the browser online with multiple players.
This project is currently inluding one board game prototype called "Skyscrapers". It is being developed alongside the platform it runs on.
The project name "tsobg" is a working project name based on my initials.

## How to Run

Requires python 3 (has been tested on version 3.8.2).
Requires some python modules including "flask".
Install flask (and other missing modules for example like this):
```
pip3 install --user flask
```

Run the prototype board game "Skyscrapers".
First, generate the card image files:
```
python3 Skyscrapers/card_graphics.py
```

This should created new folders with image files in the Skyscrapers project folder.

Now start the game:
```
python3 Skyscrapers/online/main.py
```

The command terminal should ask you to enter number of players, and then the flask will start.

Now go to the root page of the server in the browser.
You should see a page that lets you enter player name.
All players have to do this, and the game starts when playar count has filled up.

It is possible to hardcode number of players and some or all player names (also require user id's) in main.py.

### Unit Tests

Threre are some unit tests for tsobg:
```
python3 tsobg_test.py
```

## How it works

The project is divided into "tsobg" (the platform), and the board game "Skyscrapers".
The board game extends a class called "BaseGame" and implements some methods, in this case the class is called "SkyscrapersGame".
tsobg contains the web server, and the client files as well.
Once the game has started, the client game page acts as a single-page application.
The board game project (Skyscrapers) sends UI updates (called uiChanges) to the platform.
These uiChanges uses div element id's and can position divs, set size, set parent div, set colors, add a text and/or image to div etc...
The uiChanges is then picked up by the client when it asks the server platform for the latest uiChanges.
It is possible to select only a subset of players when making uiChanges, to handle for example secret information.

The board game can also add add one or more actions to a div. These should be sent back to board game object when user interacts.
If the action is valid the the board game object will progress the game by updating its state, and send new uiChanges to the clients.

### UI History, Game State History
Finally, the platform includes a uiHistory and game state history. The uiHistory makes it possible for the clients to step backwards to see what happened in the past.
The game state history should make it possible to revert one or more moves if all players agrees that this is ok to do so (when it has been implemented).