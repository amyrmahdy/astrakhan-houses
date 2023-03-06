def getSecondLevelKeys(dictionary):
    set_keys = set()
    for high_key in dictionary:
        set_keys.update(set(dictionary[high_key].keys()))
    return set_keys
