import src.Modules.Prompt_lists as P
import random

def material ():
    selected_material = list(map(str, random.choice(P.materials_list).split("~")))
    return selected_material

def shape ():
    selected_shape = random.sample(P.shape_list, random.randint(1, 3))
    return selected_shape

def color ():
    selected_color = random.sample(P.colors_list, random.randint(1, 6))
    return selected_color

def medium ():
    selected_medium = list(map(str, random.choice(P.medium_list).split("~")))
    return selected_medium

def style ():
    selected_style = list(map(str, random.choice(P.style_list).split("~")))
    return selected_style
