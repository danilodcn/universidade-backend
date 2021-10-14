
def get_attr(object: object, start_with: str, end_with: str):
    # import ipdb; ipdb.set_trace()
    
    for attr in dir(object):
        print(attr, start_with, end_with)
        if attr.startswith(start_with) and attr.endswith(end_with):
            return getattr(object, attr)