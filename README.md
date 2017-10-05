# Morpheas
Morpheas is a Blender GUI API that helps with the construction of custom GUI. It depends on BGL (Blender python module that gives access to Blender's window OpneGL context) and PyPNG

# Features

* **Simple structure , easy to learn**. Only 2 methods needed for the functioning of the GUI
* **Fully documented code**
* **Single module**. Entire source code contained only in on python source code file
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
* **OpenGL loading of textures**. Textures are **NOT** loaded using the traditional method of the image editor. This means that the user of your addon will never see his image editor getting cluttered with images he does not use. Instead Texures are loaded using OpenGL and PyOpenGL in the background completely invisible to the user of your addon
* **Custom actions** , actions assigned to events are defined as independent classes giving great deal of flexibility to the coder on defining custom functionality
* **Fully Object Orientated** , the library makes no use of globals, precedures or anything else than python classes
* **Examples**. Morpheas comes with multiple examples also fully documented and it even includes assets used by those examples in the form of a single blender file. Just install Morpheas as a regular Blender addon to demo its features through its examples found in Tools Panel , "Morpheas" tab

#Installation
Installing is very simple just add morpheas.py to your project and you are ready to use it, all code is included in a single file

You will also need [png.py](https://github.com/drj11/pypng/blob/master/code/png.py) which you can get from code folder of the [github repo of PyPNG project](https://github.com/drj11/pypng)

# Documentation

Documentation of the project is included in the source code in form of code comments. Morpheas is fully documented and it also comes included with several examples also fully documented
