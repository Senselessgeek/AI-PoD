from src.Modules.Content import material, shape, medium, color, style

def midjourney_message():
    midjourney_message = "Selected material: {}, Selected shapes: {}, Selected colors: {}, Selected medium: {}, Selected style: {}".format(material(),shape(),color(),medium(),style())
    return midjourney_message