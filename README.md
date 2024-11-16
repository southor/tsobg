
# T.S. Online Board Game

## Description

Project under development, it is a platform for testing new boardgame prototypes in the browser online with multiple players.
This project is currently including one board game prototype called "Skyscrapers".
The project name "tsobg" is a working project name.

## How to Run

Requires python 3. Has been tested on version 3.8.2 and later on 3.11.1. Not sure what the minimum version currently is.
Requires some python modules including "flask", module names are printed as errors if you try to run it.
Install flask (and other missing modules for example like this):
```
pip3 install --user flask
```

Run the prototype board game "Skyscrapers".
First, generate the graphics image files:
```
python Skyscrapers/generate_graphics.py
```

This should create new folders with image files in the Skyscrapers project folder.

Now start the game:
```
python Skyscrapers/online/main.py
```

The command terminal should ask you to enter number of players, and then the flask server will start.

Now go to the root page of the server in the browser.
You should see a page that lets you enter your player name.
All players have to do this, and the game starts when player count has filled up.

It is possible to hardcode number of players and some or all player names (also require user id's) in game_settings.py.

### Unit Tests

Threre are some unit tests for tsobg and Skyscrapers, run like this:
```
python tsobg_test.py
python Skyscrapers/Skyscrapers_test.py
```
Or run the files from an IDE.

## How it works

The project is divided into "tsobg" (the platform), and the board game "Skyscrapers".
The board game extends an interface called "GameInterface" and implements some methods, in this case the class is called "SkyscrapersGame".
tsobg contains the web server, and the client files as well.
Once the game has started, the client game page acts as a single-page application.
The board game project (Skyscrapers) sends client updates to the platform (by a reference to GameManager), these updates are sent via the "UIInterface" class.
The game project both creates and alternates the UI for the game as it goes on sending "uiChanges".
These uiChanges uses div element id's and can position divs, set size, set parent div, set background colors, add a text and/or image to div etc...
The uiChanges is picked up by the client when it asks the server platform for the latest uiChanges.
It is possible to select only a subset of players when making uiChanges, to handle for example secret information.

The game project can also add one or more actions to a div (under development). These should be sent back to board game object when user interacts.
If the action is valid the board game object will progress the game by updating its state, and send new uiChanges to the clients.

### UI History, actionHistory
Finally, the platform includes a uiHistory and player action history. The uiHistory makes it possible for the clients to step backwards to see what happened in the past.
The actionHistory makes it possible to revert one or more moves if all players agrees that this is ok to do so.
This is an expermintal feature, can be tested by first taking some actions to progress the game a couple of states,
then use the admin page to trigger a revert: http://127.0.0.1:5000/admin/<token>. Token value is set in settings.py.

### GameObject, Layouts
A higher level alternative to the ui changes model is under development.
This is a GameObject model, where the game project can create GameObjects and Layouts.
Each GameObjet corresponds to a div element in the client.
A GameObject can have other GameObjects as children, and Layout
type and its settings determine how the children are positioned.