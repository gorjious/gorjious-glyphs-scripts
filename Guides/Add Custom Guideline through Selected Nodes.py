#MenuTitle: Add Custom Guidelines through Selected Nodes
# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *
import math
__doc__ = """
Opens a menu to present options for adding guideline(s) through selected node(s) by specifying an angle. Includes presets for pre-defined angles and ratio to create guidelines quickly.
"""

#This project uses the ChatGPT model from OpenAI for natural language processing.
#ChatGPT is an AI language model that can generate text responses to a wide range of prompts.
#This project was a collaboration between ChatGPT and Gor Jihanian (@gorjious)
#Credit: OpenAI (https://openai.com/)

class AddCustomGuideline(object):
    def __init__(self):
        self.w = FloatingWindow((420, 165), "Add Custom Guidelines through Selected Nodes")
        self.w.angle_input = EditText((10, 10, 50, 22), placeholder="Angle")
        self.w.mirror_checkbox = CheckBox((70, 10, 130, 22), "Mirror angle", callback=self.mirror_angle)
        self.w.keep_open_checkbox = CheckBox((190, 10, 180, 22), "Keep window open", value=True)
        self.w.add_button = Button((10, 130, -10, 22), "Add Guideline(s) to selected nodes", callback=self.add_guideline)
        self.w.add_0_button = Button((10, 40, 50, 22), "0°", callback=self.add_0_guideline)
        self.w.add_30_button = Button((70, 40, 50, 22), "30°", callback=self.add_30_guideline)
        self.w.add_45_button = Button((130, 40, 50, 22), "45°", callback=self.add_45_guideline)
        self.w.add_60_button = Button((190, 40, 50, 22), "60°", callback=self.add_60_guideline)
        self.w.add_90_button = Button((250, 40, 50, 22), "90°", callback=self.add_90_guideline)
        
        self.w.add_italic_button = Button((310, 40, 100, 22), "Italic Angle", callback=self.add_italic_guideline)
        
        self.w.add_10_1_button = Button((10, 70, 50, 22), "10:1", callback=self.add_10_1_guideline)
        self.w.add_9_1_button = Button((70, 70, 50, 22), "9:1", callback=self.add_9_1_guideline)
        self.w.add_8_1_button = Button((130, 70, 50, 22), "8:1", callback=self.add_8_1_guideline)
        self.w.add_7_1_button = Button((190, 70, 50, 22), "7:1", callback=self.add_7_1_guideline)
        self.w.add_6_1_button = Button((250, 70, 50, 22), "6:1", callback=self.add_6_1_guideline)
        self.w.add_5_1_button = Button((10, 100, 50, 22), "5:1", callback=self.add_5_1_guideline)
        self.w.add_4_1_button = Button((70, 100, 50, 22), "4:1", callback=self.add_4_1_guideline)
        self.w.add_3_1_button = Button((130, 100, 50, 22), "3:1", callback=self.add_3_1_guideline)
        self.w.add_2_1_button = Button((190, 100, 50, 22), "2:1", callback=self.add_2_1_guideline)
        self.w.add_3_2_button = Button((250, 100, 50, 22), "3:2", callback=self.add_3_2_guideline)
        self.w.zero_button = Button((310, 70, 100, 22), "Zero V/H", callback=self.zero_guidelines)
        self.w.delete_button = Button((-110, 100, -10, 22), "Delete All", callback=self.delete_guidelines_from_selected_layer)
        self.w.open()
        
    def delete_guidelines_from_selected_layer(self, sender):
        font = Glyphs.font
        selected_layers = font.selectedLayers
        if len(selected_layers) > 0:
            for layer in selected_layers:
                if len(layer.guides) > 0:
                    layer.guides = []
#                    Message("Guidelines deleted", "Local guidelines have been deleted from the selected layer.")
                    print("Guidelines deleted", "Local guidelines have been deleted from the selected layer.")
                else:
                    Message("No guidelines to delete", "There are no local guidelines on the selected layer.")
        else:
            Message("No layer selected", "Please select at least one layer in the Edit view.")



    def zero_guidelines(self, sender):
        font = Glyphs.font
        selected_layer = font.selectedLayers[0]
        for guide in selected_layer.guides:
            if guide.angle == 90:
                guide.position = (guide.position[0], 0)
            elif abs(guide.angle) == 0:
                guide.position = (0, guide.position[1])
                
    def check_guideline_exists(self, layer, node, angle):
        for guide in layer.guides:
            if node is None:
                if guide.angle == angle:
                    return True
            elif guide.position == node.position and guide.angle == angle:
                return True
        return False
    def mirror_angle(self, sender):
        angle_input = self.w.angle_input.get()
        if angle_input:
            try:
                angle = float(angle_input)
            except ValueError:
                Message("Invalid input", "Please enter a valid numeric value for the angle degree.")
                return
            if sender.get():
                self.w.angle_input.set(str(-angle))
            else:
                self.w.angle_input.set(str(abs(angle)))
                

    def add_guideline(self, sender):
        angle_input = self.w.angle_input.get()
        if angle_input:
            try:
                angle = float(angle_input)
            except ValueError:
                Message("Invalid input", "Please enter a valid numeric value for the angle degree.")
                return
            font = Glyphs.font
            selected_glyphs = font.selectedLayers
            if len(selected_glyphs) > 0:
                for layer in selected_glyphs:
                    if len(layer.selection) > 0:
                        for node in layer.selection:
                            if not self.check_guideline_exists(layer, node, angle):
                                guideline = GSGuideLine()
                                guideline.position = node.position
                                guideline.angle = angle
                                layer.guides.append(guideline)
                            else:
                                print(f"Guideline already exists on node {node.position} at angle {angle}")
                    else:
                        if not self.check_guideline_exists(layer, None, angle):
                            guideline = GSGuideLine()
                            guideline.position = (0, 0)
                            guideline.angle = angle
                            layer.guides.append(guideline)
                        else:
                            print(f"Guideline already exists on layer {layer.name} at angle {angle}")
            else:
                Message("No layer selected", "Please select at least one layer in the Edit view.")
            if not self.w.keep_open_checkbox.get():
                self.w.close()

    #PRESETS: ANGLES
    def add_0_guideline(self, sender):
        angle = 0
        self.add_guideline_with_mirror(angle)
    def add_30_guideline(self, sender):
        angle = 30
        self.add_guideline_with_mirror(angle)
    def add_45_guideline(self, sender):
        angle = 45
        self.add_guideline_with_mirror(angle)
    def add_60_guideline(self, sender):
        angle = 60
        self.add_guideline_with_mirror(angle)
    def add_90_guideline(self, sender):
        angle = 90
        self.add_guideline_with_mirror(angle)

    #PRESETS: RATIOS
    def add_10_1_guideline(self, sender):
        angle = math.degrees(math.atan(10/1))
        self.add_guideline_with_mirror(angle)
    def add_9_1_guideline(self, sender):
        angle = math.degrees(math.atan(9/1))
        self.add_guideline_with_mirror(angle)
    def add_8_1_guideline(self, sender):
        angle = math.degrees(math.atan(8/1))
        self.add_guideline_with_mirror(angle)
    def add_7_1_guideline(self, sender):
        angle = math.degrees(math.atan(7/1))
        self.add_guideline_with_mirror(angle)  
    def add_6_1_guideline(self, sender):
        angle = math.degrees(math.atan(6/1))
        self.add_guideline_with_mirror(angle)
    def add_5_1_guideline(self, sender):
        angle = math.degrees(math.atan(5/1))
        self.add_guideline_with_mirror(angle)
    def add_4_1_guideline(self, sender):
        angle = math.degrees(math.atan(4/1))
        self.add_guideline_with_mirror(angle)
    def add_3_1_guideline(self, sender):
        angle = math.degrees(math.atan(3/1))
        self.add_guideline_with_mirror(angle)
    def add_2_1_guideline(self, sender):
        angle = math.degrees(math.atan(2/1))
        self.add_guideline_with_mirror(angle)
    def add_3_2_guideline(self, sender):
        angle = math.degrees(math.atan(3/2))
        self.add_guideline_with_mirror(angle)

    def add_italic_guideline(self, sender):
        font = Glyphs.font
        selected_layer = font.selectedLayers[0]
        italic_angle = selected_layer.master.italicAngle
        guideline = GSGuideLine()
        guideline.position = (0, 0)
        italic_angle = 90 - italic_angle
        guideline.angle = italic_angle
        font = Glyphs.font
        selected_glyphs = font.selectedLayers
        angle = italic_angle
        mirror = self.w.mirror_checkbox.get()
        if mirror:
            angle = -angle
        if len(selected_glyphs) > 0:
            for layer in selected_glyphs:
                if len(layer.selection) > 0:
                    for node in layer.selection:
                        if not self.check_guideline_exists(layer, node, angle):
                            guideline = GSGuideLine()
                            guideline.position = node.position
                            guideline.angle = angle
                            layer.guides.append(guideline)
                        else:
                            print(f"Guideline already exists on node {node.position} at angle {angle}")
                else:
                    if not self.check_guideline_exists(layer, None, angle):
                        guideline = GSGuideLine()
                        guideline.position = (0, 0)
                        guideline.angle = angle
                        layer.guides.append(guideline)
                    else:
                        print(f"Guideline already exists on layer {layer.name} at angle {angle}")
        else:
            Message("No layer selected", "Please select at least one layer in the Edit view.")
        if not self.w.keep_open_checkbox.get():
            self.w.close()

    def add_guideline_with_mirror(self, angle):
        mirror = self.w.mirror_checkbox.get()
        if mirror:
            angle = -angle
        font = Glyphs.font
        selected_glyphs = font.selectedLayers
        if len(selected_glyphs) > 0:
            for layer in selected_glyphs:
                if len(layer.selection) > 0:
                    for node in layer.selection:
                        if not self.check_guideline_exists(layer, node, angle):
                            guideline = GSGuideLine()
                            guideline.position = node.position
                            guideline.angle = angle
                            layer.guides.append(guideline)
                        else:
                            print(f"Guideline already exists on node {node.position} at angle {angle}")
                else:
                    if not self.check_guideline_exists(layer, None, angle):
                        guideline = GSGuideLine()
                        guideline.position = (0, 0)
                        guideline.angle = angle
                        layer.guides.append(guideline)
                    else:
                        print(f"Guideline already exists on layer {layer.name} at angle {angle}")
        else:
            Message("No layer selected", "Please select at least one layer in the Edit view.")
        if not self.w.keep_open_checkbox.get():
            self.w.close()

AddCustomGuideline()
