from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional

from ..__utils__.copy import jsoncopy, merge_filters
from ..__utils__.parsers import parse_to_clarify_filter

from pyclarify import Item, Signal, query


@dataclass
class Attribute:
    meta: Item
    filter: query.Filter = field(default_factory=dict)
    add_filter: query.Filter = field(default_factory=dict)
    signals: Optional[list[Signal]] = field(default_factory=list)
    independent: bool = False  # Ignore parent filters
    name: str = None
    labels: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.name:
            if self.meta:
                self.meta.name = self.name
            else:
                self.meta = Item(name=self.name)
        if self.add_filter:
            self.filter = merge_filters(self.filter, self.add_filter)
            self.add_filter = {}

    def copy(
        self,
        meta=None,
        name=None,
        labels=None,
        filter=None,
        signals=None,
        independent=None,
    ):
        if not meta:
            meta = deepcopy(self.meta)
        if name:
            meta.name = name
        if labels:
            meta.labels = labels
        if not filter:
            filter = jsoncopy(self.filter)
        if not signals:
            signals = deepcopy(self.signals)
        if not independent:
            independent = self.independent
        return Attribute(meta, filter, signals, independent=independent)

    def to_clarify_filter(self):
        return parse_to_clarify_filter(self.filter)

    def add_signal(self, signals):
        if signals:
            if not isinstance(signals, list):
                signals = [signals]
            else:
                if isinstance(signals[0], list):
                    signals = [s for l in signals for s in l]
            for signal in signals:
                if signal not in self.signals:
                    self.signals += [signal]

    def __str__(self):
        return self.meta.name

    def __hash__(self):
        return hash(tuple(self))
