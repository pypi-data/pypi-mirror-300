import json


def jsoncopy(dictionary):
    return json.loads(json.dumps(dictionary))


def merge_labels(self_labels, other_labels, return_dictionary=False):
    # returns list by default
    labels = []
    if self_labels:
        labels += self_labels
    if other_labels:
        labels += other_labels
    dictionary = {}
    for label in labels:
        label = {list(label.keys())[0]: [list(label.values())[0]]}
        dictionary = dictionary | label
    if return_dictionary:
        return dictionary
    return [{k: v[0]} for k, v in dictionary.items()]


def merge_filters(self_filter, other_filter):
    """
    :meta private:

    Merges two clarify filters to a single filter

    Parameters
    ----------
        self_filter: Dict
            ...

        other_filter: Dict
            ...
    Example
    -------
        ...

    """
    self_filter = jsoncopy(self_filter)
    parent_filter = jsoncopy(other_filter)
    if self_filter and parent_filter:
        if "$and" in self_filter.keys():
            self_filter = self_filter["$and"]
        else:
            self_filter = [self_filter]

        if "$and" in parent_filter.keys():
            parent_filter = parent_filter["$and"]
        else:
            parent_filter = [parent_filter]

        self_keys = [list(sf.keys())[0] for sf in self_filter]

        for f in parent_filter:
            f_key = list(f.keys())[0]
            if f_key not in self_keys:
                self_filter += [f]
            else:
                indx = self_keys.index(f_key)
                # pop overlapping element
                self_filter.pop(indx)
                self_filter.insert(indx, f)
        if len(self_filter) == 1:
            return self_filter[0]
        return {"$and": self_filter}

    elif parent_filter:
        return parent_filter
    return self_filter
