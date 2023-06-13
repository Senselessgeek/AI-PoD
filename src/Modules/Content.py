import Modules.Prompt_lists as P
import random

def material ():
    selected_material = random.choice(P.materials_list)
    return selected_material

def shape () :
    selected_shape = random.sample(P.shape_list, random.randint(1, 3))
    return selected_shape

def color () :
    selected_color = random.sample(P.colors_list, random.randint(1, 6))
    return selected_color

def medium () :
    selected_medium = random.choice(P.medium_list)
    return selected_medium
