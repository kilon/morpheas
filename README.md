# Morpheas
Morpheas is a GUI API based on OpenGL for the creation of guis that use skins, which are plain PNG files. Morpheas is designed to mainly work with Blender but its architecture supports usage outside Blender as well.
# Features
* **live coding GUI API** , Moprheas takes advantage of my livecoding library which means you can create and code GUIs real time , without any delays
* **Simple structure , easy to learn**. Only 2 methods needed for the functioning of the GUI
* **Fully documented code**. Code comments for the entire code.
* **Modular architecture**. Through its backend module, Morpheas can support many applications and does not depend only on Blender
* **trasnparent or non trasparent custom skins (textures) for any GUI element**
* **Text with customisable size and font**
* **Buttons with the ability to change skin when mouse enters or exits them**
* **Auto hide feature** that hides the GUI when the mouse exits the area assigned with drawing the GUI
* **Relative and absolute coordinate system**. Relative system coordinate system starts from the bottom left corner of the area assigned for drawing the GUI. Absolute coordinate system start from the bottom left area of entire Blender window. This way you can very precisely locate GUI elements
* **Independent event system** supporting, left click, left click release, right click, right click release, mouse move , mouse over and mouse outside the graphical element
* **Multi layer system** that allows Morphs ( the basic Morpheas GUI element) to include other morphes as children
* World morph provides **automatic handling of Blender events and drawing of Morpheas**
* **Non Blocking**. Blender events not used are passed back to Blender so that Morpheas **NEVER** interfere with normal user blender interaction 
* **Multiple textures**. Each morph can have multiple textures assigned to it, one is only active at a time
* **OpenGL loading of textures**. Skins/textures are loaded directly to the graphic card memory to take full advantage of the GPU
* **Custom actions** , actions assigned to events are defined as independent classes giving great deal of flexibility to the coder on defining custom functionality
* **Fully Object Orientated** , the library makes no use of globals, precedures or anything else than python classes
* **Examples**. Morpheas comes with multiple examples also fully documented and it even includes assets used by those examples in the form of a single blender file. Just install Morpheas as a regular Blender addon to demo its features through its examples found in Tools Panel , "Morpheas" tab

# Installation

Morphease only dependency is that of the livecoding library which can be found at

https://github.com/kilon/livecoding

Your project should be structured as such that it contains two folders, one named morpheas and another named livecoding
# Documentation

Documentation of the project is included in the source code in form of code comments. Morpheas is fully documented and it also comes included with several examples also fully documented

Seperate documentation is a still a WIP for those prefering a more traditional format
