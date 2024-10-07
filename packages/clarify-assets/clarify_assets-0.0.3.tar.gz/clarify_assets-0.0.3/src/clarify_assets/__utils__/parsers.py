from .copy import jsoncopy
from .validators import is_leaf
import json


def parse_to_sqlite3(obj, key_list, hash_key=None):
    format = []
    for k in key_list:
        if k == "HashKey":
            v = hash_key
        elif k in obj.keys():
            v = obj[k]
        else:
            v = None
        if isinstance(v, list):
            if v != []:
                v = v[0]
            else:
                v = None
        format.append(v)
    return format


# Modifying signals for lookups
def flatten(signal):
    d_signal = signal.model_dump(mode="json")
    d_signal = d_signal.pop("attributes")
    d_signal["id"] = signal.id
    # DO NOT SUPPORT ENUM VALUES
    d_signal.pop("enumValues")
    label_copy = jsoncopy(d_signal["labels"])

    for key in label_copy.keys():
        d_signal[key] = label_copy[key]
    del label_copy
    d_signal.pop("labels")
    return d_signal


def scuffed_filter_key_extraction(filter):
    if "$and" in filter.keys():
        filters = str(filter["$and"]).split(",")
    else:
        return list(filter.keys())

    filter_keys = []
    for f in filters:
        f = f.strip()

        if f[0] == "[":
            f = f[1:]
        if f[-1] == "]":
            f = f[:-1]
        try:
            f = eval(f)
            f = list(f.keys())[0]
            f = f.replace("labels.", "")
            filter_keys += [f]
        except:
            pass
    return filter_keys


def parse_filter(filter):
    key = list(filter.keys())[0]
    value = list(filter.values())[0]
    if key == "$and":
        filter = filter["$and"]
        string = ""
        for _filter in filter:
            string += parse_filter(_filter) + " AND "
        return string[:-5]
    elif key == "$or":
        filter = filter["$or"]
        for _filter in filter:
            string += parse_filter(_filter) + " OR "
        return string[:-4]
    else:

        operator = "$eq"

        if isinstance(value, dict):
            operator = list(value.keys())[0]
            value = list(value.values())[0]
        key = key.replace("-", "_").replace("labels.", "")
        match operator:
            case "$eq":
                if isinstance(value, list):
                    value = value[0]
                return f"{key} == '{value}'"

            case "$ne":
                if isinstance(value, list):
                    value = value[0]
                return f"{key} != '{value}'"

            case "$in":
                return f'{key} IN {str(value).replace("[", "(").replace("]", ")")}'

            case "$nin":
                return f'{key} NOT IN {str(value).replace("[", "(").replace("]", ")")}'

            case "$regex":
                if isinstance(value, list):
                    value = value[0]
                return f"REGEXP({key}, '{value}')"
        return False


def get_all_keys(look_up_list):
    set_of_keys = set()
    for item in look_up_list:
        for k in item.keys():
            set_of_keys.add(k)
    set_of_keys.add("HashKey")
    return set_of_keys


def update_leaf_value(leaf):
    key = list(leaf.keys())[0]
    value = list(leaf.values())[0]
    if isinstance(value, list):
        value = value[0]
    return value


def iterate_sub_dict(s):
    key = list(s.keys())[0]
    value = list(s.values())[0]
    if is_leaf(s):
        # clean_labels
        if key.startswith("labels"):
            value = update_leaf_value(s)
        return {key: value}
    else:
        return {key: [iterate_sub_dict(s) for s in value]}


def parse_to_clarify_filter(filter):
    my_new_dict = {}
    if filter:
        tmp_filter = jsoncopy(filter)
        my_new_dict = iterate_sub_dict(tmp_filter)
    return json.dumps(my_new_dict)
