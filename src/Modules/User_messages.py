from src.Modules.Content import material, shape, medium, color

def midjourney_message():
    midjourney_message = "Selected material: {}, Selected shapes: {}, Selected colors: {}, Selected medium: {}".format(material(),shape(),color(),medium())
    return midjourney_message