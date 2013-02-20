methodo-carpo
=============

Sublime Text 2 Plugin

PHP ONLY
========

PHP Method Grabber

Notes and Issues:
	Working on a way to only have to press the period one time. 
	For some reason if you only press it one time the event is ran before the list is built.

	There is undesirable behavior when using "." in other places such as:
		If you type "." in the middle of a string it sends the cursor to the end of the line.
		When you edit a concatination it will send the cursor to the end of the  line.




Usage:
======
Pressing ".." after object opens ST2's autocomplete.

Features
========

For us programmers that are die hard dot syntax guys and don't like having to type the arrow.(I know we are lazy, but I am a creature of habit.)

The ".." is replaced with the "->" symbol.

Upon the second press of the period Sublime's autocomplete is opened containing only the methods that are associated with that object.

Notifies you when you mistype an object identifier. 


Upcoming features: 
==================

For you die hard guys that just have to type the "->" to access your object methods there will shortly be functionality for that as well.

Access to parent/base class methods.





