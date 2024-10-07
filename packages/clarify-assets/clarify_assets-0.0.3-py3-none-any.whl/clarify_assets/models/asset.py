from dataclasses import dataclass, field
from typing import Optional
from pyclarify import query
from copy import deepcopy

from ..__utils__.copy import jsoncopy, merge_filters, merge_labels
from ..__utils__.parsers import parse_to_clarify_filter
from .attribute import Attribute


@dataclass
class Asset:
    parent: Optional["Asset"] = None  # Can only have one parent
    children: Optional[list["Asset"]] = field(
        default_factory=list
    )  # can have multiple children
    labels: list[str] = field(default_factory=list)
    filter: list[query.Filter] = field(default_factory=list)
    attributes: Optional[list[Attribute]] = field(default_factory=list)
    independent: bool = False

    def __post_init__(self):
        if self.parent:
            self.labels = merge_labels(self.labels, self.parent.labels)
            if not self.independent:
                self.filter = merge_filters(self.filter, self.parent.filter)

            if self.parent.children:
                if self not in self.parent.children:
                    self.parent.children += [self]
            else:
                self.parent.children = [self]

            # EXPERIMENTAL
            attr_name = list(self.labels[0].values())[0].lower().replace(" ", "_")
            if not hasattr(self.parent, attr_name):
                setattr(self.parent, attr_name, self)

        # update filter for attributes
        if self.attributes:
            for attr in self.attributes:
                attr_name = str(attr)
                if not hasattr(self.parent, attr_name):
                    setattr(self, attr_name, attr)
                attr.meta.labels = merge_labels(
                    attr.labels, self.labels, return_dictionary=True
                )
                attr.labels = merge_labels(attr.labels, self.labels)

                if not attr.independent:  # ignore parent filters
                    if attr.filter:
                        attr.filter = merge_filters(attr.filter, self.filter)
                    else:
                        attr.filter = self.filter

    def __eq__(self, other):
        return self.labels == other.labels and self.filter == other.filter

    def __hash__(self):
        return hash(str(self))

    def to_clarify_filter(self):
        return parse_to_clarify_filter(self.filter)

    def append(self, child_asset_or_attribute):
        if isinstance(child_asset_or_attribute, list):
            for obj in child_asset_or_attribute:
                self.append(obj)
        elif isinstance(child_asset_or_attribute, self.__class__):
            self.children.append(child_asset_or_attribute)
            self.link_tree()
            self.children = list(set(self.children))
        elif isinstance(child_asset_or_attribute, Attribute):
            self.attributes.append(child_asset_or_attribute)
            self.link_tree()
            self.attributes = list(set(self.attributes))

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        else:
            return self

    def assert_parents(self):
        if self.children:
            for child in self.children:
                child.parent = self
                self.__post_init__()
                child.assert_parents()
        else:
            self.__post_init__()
            if self.attributes:
                for attr in self.attributes:
                    attr.__post_init__()

    def link_tree(self):
        root = self.get_root()
        root.assert_parents()

    def __str__(self):
        return str(list(self.labels[0].values())[0])

    def generate_string(
        self, debug=False, minimal=False, only_failures=False, indent=0
    ):
        STAR = " \u2605 "
        CHECK = " \u2713 "
        CROSS = " \u2718 "
        ARROW = " \u2192 "
        GREEN = "\033[1;32m"
        ORANGE = "\033[1;33m"
        RED = "\033[1;31m"
        NEW_LINE_RESET = "\033[0;30m\n"
        string = ""
        current_asset = list(self.labels[0].values())[0]

        if self.attributes:
            if minimal:
                if len(self.attributes) == sum(
                    [len(attr.signals) for attr in self.attributes]
                ):
                    if not only_failures:
                        string += GREEN + current_asset + CHECK

                else:
                    string += RED + current_asset + CROSS
            if debug:
                if not minimal:
                    string += current_asset + NEW_LINE_RESET
                    indent += 1
                    # TODO: Add sorting of attributes
                    for attr in self.attributes:
                        string += ARROW * indent + str(attr.meta.name) + "\n"
                        if attr.signals:
                            if len(attr.signals) == 1:
                                string += (
                                    ARROW * (indent + 1)
                                    + STAR
                                    + GREEN
                                    + str(attr.signals[0].attributes.name)
                                    + NEW_LINE_RESET
                                )
                            else:
                                string += (
                                    ARROW * (indent + 1)
                                    + STAR
                                    + RED
                                    + str(attr.to_clarify_filter())
                                    + NEW_LINE_RESET
                                )
                                if debug:
                                    for s in attr.signals:
                                        string += (
                                            ARROW * (indent + 1)
                                            + STAR
                                            + RED
                                            + str(s.attributes.name)
                                            + str(s.attributes.labels)
                                            + NEW_LINE_RESET
                                        )
                        else:
                            # Print filter as well
                            string += (
                                ARROW * (indent + 1)
                                + STAR
                                + ORANGE
                                + str(attr.to_clarify_filter())
                                + NEW_LINE_RESET
                            )
                    indent -= 1
                else:
                    if not len(self.attributes) == sum(
                        [len(attr.signals) for attr in self.attributes]
                    ):
                        string += NEW_LINE_RESET
                        indent += 1
                        # TODO: Add sorting of attributes
                        for attr in self.attributes:
                            string += ARROW * indent + str(attr.meta.name) + "\n"
                            if attr.signals:
                                if len(attr.signals) == 1:
                                    string += (
                                        ARROW * (indent + 1)
                                        + STAR
                                        + GREEN
                                        + str(attr.signals[0].attributes.name)
                                        + NEW_LINE_RESET
                                    )
                                else:
                                    string += (
                                        ARROW * (indent + 1)
                                        + STAR
                                        + RED
                                        + str(attr.to_clarify_filter())
                                        + NEW_LINE_RESET
                                    )
                                    if debug:
                                        for s in attr.signals:
                                            string += (
                                                ARROW * (indent + 1)
                                                + STAR
                                                + RED
                                                + str(s.attributes.name)
                                                + str(s.attributes.labels)
                                                + NEW_LINE_RESET
                                            )
                            else:
                                # Print filter as well
                                string += (
                                    ARROW * (indent + 1)
                                    + STAR
                                    + ORANGE
                                    + str(attr.to_clarify_filter())
                                    + NEW_LINE_RESET
                                )
                        indent -= 1
        else:
            string += current_asset
        if self.children:
            indent += 1
            # TODO: Add sorting of children
            if string == "":
                string += current_asset
            for child in self.children:
                string += child.generate_string(
                    debug=debug,
                    minimal=minimal,
                    only_failures=only_failures,
                    indent=indent,
                )
        indent -= 1
        if string != "" and string != NEW_LINE_RESET:
            string = NEW_LINE_RESET + ARROW * indent + string + NEW_LINE_RESET
        return string

    def pretty_print(self, debug=False, minimal=False, only_failures=False):
        # Clean up some logic
        if only_failures:
            debug = True
            minimal = True

        print(
            self.generate_string(
                debug=debug, minimal=minimal, only_failures=only_failures, indent=0
            )
        )

    def copy(
        self, parent=None, children=None, labels=None, filter=None, attributes=None
    ):
        if not parent:
            parent = deepcopy(self.parent)
        if not children:
            children = deepcopy(self.children)
        if not labels:
            labels = jsoncopy(self.labels)
        if not filter:
            filter = jsoncopy(self.filter)
        if not attributes:
            attributes = deepcopy(self.attributes)
        return Asset(parent, children, labels, filter, attributes)
