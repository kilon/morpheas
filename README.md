# Morpheas
Morpheas is a Blender API that helps with the construction of custom guis

# Installation
Installing is very simple just add morpheas.py to your project and you are ready to use it, all code is included in a single file

You will also need [png.py](https://github.com/drj11/pypng/blob/master/code/png.py) which you can get from code folder of the [github repo of PyPNG project](https://github.com/drj11/pypng)

# Basic usage

I am in the process of making my first commercial addon which I call "Cyclops". It will be an addon that will first target boolean and later I hope much more. 

When I started creating the Cyclops GUI it was clear that Blender GUI would not be enough for the flexibility that I wanted so the alternative solution was to use BGL. 

For those never worked with BGL, BGL is basically a blender python module which wraps the OpenGL context of Blender window and allow you to do anything you want. Essentially you draw graphics on top of Blender window, however because of Blender Python API this is very powerful and you can create your own GUI or lay on top a modification of the existing one, sky is the limit.

So In the process of doing that I created Morpheas which acts as a very small library that makes it easy to make GUIs using textures. Morpheas also has the additional advantage that bypasses the default method of loading textures with BGL which loads them in Blender image editor and from there to OpenGL. Morpheas loads them directly to OpenGL which means no need to bloat your image editor.

Right now Morpheas has the bare basics, it has basic elements that calls Morph. A Morph can be anything a picture , a button, text etc. Morph has several subclasses.

World - This morph is the collector, it collects all the morphs and passes event, its not meant to visible , its there to act as a container and general control system. You need only one World where all your Morphs will be added with the addMorph() method . World also passes events to its sub morphs , through its OnEvent() method. Its possinle also to have multiple World, each one representing a complete GUI.

ButtonMorph - A Morph that can change its appearance when the mouse enters or exits its region but also can perform an action when its clicked.

StringMoprh - A Morph to display text on screen

Morph - This is the big one that implement basic functionality for all morphs. This includes:

1) Loading textures to OpenGL using the PyPNG library. Because the textures are png they can be also partially transparent which helps when layering with other morphs.
2) Handle events with OnEvent method that then seperates them to left click, right click, mouse in and mouse out events with corresponing methods. Its possible to disable some events.
3) Children - a Morph can act as a container for other Morphs, those morphs can be accessed through the children attribute , the Morph also can access its parent and the World it belongs to with the corresponing instance variables
4) Draw - this is the actual method that draws the graphics of the Morph, it uses BGL and is expected to work inside a OpenGL context which means a modal operator usually but it could work without it though that I have not tested. Draw is not be called directly instead its called by World.draw because the World also handle the drawing of Morphs.

The Library is meant to be used from inside a modal operator as I said it may work also without a modal operator. You need only World.draw() and World.OnEvent , World.draw() is called inside the method or fuction you have assigned to the draw handle of the modal operator , while World.onEvent(event) is called inside the modal method of the modal operator where event is the same argument that modal method uses which represents the Blender events. If the Event is not handled by Morpheas , because for example the mouse is not on top of a morph or its on top of a morph that has event handling disabled it can be passed back to Blender. This means that the user can interect with a Morphic GUI without losing interaction with the existing Blender GUI.

Morpheas is made to work seamessly with the existing Blender GUI

Morpheas is still very much a WIP , in super early stage and will keep evolving together with Cyclops 
