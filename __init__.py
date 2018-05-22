# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# ===============================================================
# Copyright 2017 Dimitris Chloupis
# ================================================================
#################################################################
#
# MORPHEAS
# =================================================================
# Morpheas is a GUI API for Blender addons that takes advantage of
# BGL module that gives access to Blender OpenGL content. In turn
# this allows the user to control and manipulate the Blender GUI
# in an extreme level. Morpheas try to make this whole process
# more easy.
#################################################################
#
# Installation
# ----------------------------------------------------------------
# Installation is very simple all you have to do is copy this file
# to the same folder as your addon. Morpheas comes also with its own
# distribution of PIL included to faciliate the loading of textures
##################################################################
#
# Documentation
# ----------------------------------------------------------------
# Documentation is included in this source file because its far
# more useful to learn how Morpheas works by examining its code.
# I tried to make my intentions in code as obvious as possible
# together with providing detailed comments
#################################################################
# ================================================================



from .. import pylivecoding
from . import backend,core,tests
from .PIL import Image

live_environment = pylivecoding.LiveEnvironment()
live_environment.live_modules=["pylivecoding","morpheas.backend","morpheas.core","morpheas.tests"]
