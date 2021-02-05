def is_tuple_or_list(value) -> bool:
    """
    Check if iterable is tuple or list
    """
    return isinstance(value, list) or isinstance(value, tuple)
