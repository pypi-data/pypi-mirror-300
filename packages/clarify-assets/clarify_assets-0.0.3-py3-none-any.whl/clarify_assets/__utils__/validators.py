from pyclarify.fields.query import Operators

def can_be_published(leaf):
    return leaf.signals != []


def get_item_id_or_none(leaf):
    if leaf.signals:
        if leaf.signals[0].relationships:
            if leaf.signals[0].relationships.item:
                if leaf.signals[0].relationships.item.data:
                    if leaf.signals[0].relationships.item.data.id:
                        return leaf.signals[0].relationships.item.data.id
    return None


def compare_labels(leaf, item):
    item_labels = []
    leaf_labels = []
    for k, v in leaf.meta.labels.items():
        if v:
            leaf_labels.append((k, v[0]))
        else:
            leaf_labels.append((k, ""))
    for k, v in item.attributes.labels.items():
        if v:
            item_labels.append((k, v[0]))
        else:
            item_labels.append((k, ""))
    set1 = set(leaf_labels)
    set2 = set(item_labels)
    new_label = list(set1 - set2)
    removed_label = list(set2 - set1)
    return new_label, removed_label


def compare_meta_and_published_item(leaf, item):
    new_labels, removed_labels = compare_labels(leaf, item)
    if leaf.meta.name != item.attributes.name:
        new_labels.append(("name", leaf.meta.name))
        removed_labels.append(("name", item.attributes.name))
    if leaf.meta.engUnit != item.attributes.engUnit:
        new_labels.append(("engUnit", leaf.meta.engUnit))
        removed_labels.append(("engUnit", item.attributes.engUnit))
    if leaf.meta.valueType != item.attributes.valueType:
        new_labels.append(("valueType", leaf.meta.valueType))
        removed_labels.append(("valueType", item.attributes.valueType))
    return new_labels, removed_labels


def is_leaf(obj):
    if isinstance(obj, dict):
        # check value
        keys = list(obj.keys())
        if len(keys) != 1:
            return False

        # check only child
        value = obj[keys[0]]
        if keys[0].startswith("labels"):
            return True

        # is string obj is eq
        if isinstance(value, str):
            return True

        if isinstance(value, list):
            return False

        if isinstance(value, dict):
            # check for operator
            keys = list(value.keys())

            if len(keys) != 1:
                return False

            try:
                op = Operators(keys[0])
                return True
            except:
                return False
