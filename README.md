methodo-carpo
=============

Sublime Text 2 Plugin

PHP Method Grabber

Functionality Goals:



Look up PHP Class files in current directory



2013-02-17  Currenty under development.

Notes:
	Working on a way to only have to press the period one time. 
	For some reason if you only press it one time the event is ran before the list is built.



Usage:
======
Pressing ".." after object opens ST2's autocomplete.

Features
========

For us programmers that are die hard dot syntax guys and don't like having to type the arrow.(I know we are lazy, but I am a creature of habit.)

The ".." is replaced with the "->" symbol.

Upon the second press of the period Sublime's autocomplete is opened containing only the methods that are associated with that object.

Notes:
==========

Currently the class file must reside in the same Directory as the file you are working on.  This will be changed very shortly to recursively search the project for the class file.

Upcoming features: 
==================

For you die hard guys that just have to type the "->" to access your object methods there will shortly be functionality for that as well.

Access to parent/base class methods.





