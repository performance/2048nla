2048nla
=======

AI for 2048 with no look ahead.

* Solve the 2048 puzzle without using any look ahead
* ie no wondering what it would be like to make a particular move
* especially we do not want to virtually take moves and then select the best move based on the virtual results
* the approach we want is similar to a closed form solution, but is actually rule based 


Python source derived from [ 2048-ai ]( https://github.com/nneonneo/2048-ai )

## Running the browser-control version

* Install the firefox extension [Remote Control for Firefox](https://addons.mozilla.org/en-US/firefox/addon/remote-control/).
* Customize firefox such that the new RemoteControl Icon is visible on the address bar
* Open the [ original 2048 game ]( http://gabrielecirulli.github.io/2048/ ) or its local copy in a tab in firefox.
* Make sure that is the currently active tab and press the remote control button such that it turns green.
* From a Terminal navigate to the source ocde of this project and run 
* $python per.py
* Watch how it tries to solve the puzzle


## How to contribute

* Play the [ original 2048 game ]( http://gabrielecirulli.github.io/2048/ )
* Try to think of ways to solve it without contemplating what a move could potentially do.
* Try to summarize your approach as a set of rules
* Run the code in this project as per the description above. ( Try atleast 16 runs ).
* Go through the code and make your changes, test thoroughly and submit your patches or pull request.
* I will accept any change that helps the project get better, architecture, style, logic, performance, anything 

