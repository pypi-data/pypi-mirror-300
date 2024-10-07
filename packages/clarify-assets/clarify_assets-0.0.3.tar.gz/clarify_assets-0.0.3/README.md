# clarify-assets

Populate Clarify metadata through asset models.

### Flow example

```python
from clarify_assets import Asset, Attribute, AssetBroker
from pyclarify import Item


enterprise = Asset(
    labels = [{"enterprise": "OG Inc"}]
)

station = Asset(
    labels = [{"station": "work"}]
)

temperature = Attribute(
    meta=Item(
        name="Temperature",
        labels={
            "medium": ["Air"]
        }
    ),
    filter = {"name": "Temperature"}
)

climate = Asset(
    labels=[{"cell": "climate"}],
    attributes=[temperature]
)

station.append(climate)
enterprise.append(station)

enterprise.pretty_print(debug=True)

AB = AssetBroker(
    credentials="credentials.json",
    integrations=["integration1"]
)

AB.flush_and_build_db()

AB.assign_signals(enterprise)

enterprise.pretty_print(minimal=True)

AB.publish_asset(enterprise)
```

### Custom attribute example

```python
from clarify_assets import Attribute
from dataclasses import dataclass

def get_value_or_none(key, asset):
  return list(filter(lambda x: x,
            list(map(lambda x: x[key] if key in x.keys() else None,
                     asset.labels)
                )
  ))

def get_line_number(string):
  return string.lower().replace(" ", "").split("line")[-1]


@dataclass
class FishtalkAttribute(Attribute):
  def __post_init__(self):
    super().__post_init__()
    self.independent = True
    if self.meta:
      i = self.meta.dict()
      i["labels"]["data-source"] = ["Fishtalk"]
      self.meta = Item(**i)
    if self.labels:

      area_label = get_value_or_none("area", self)
      line_label = get_value_or_none("line", self)
      if area_label and line_label:
        line_no =  get_line_number(line_label)
        if len(line_no) == 1:
          line_no = "0" + line_no

        unit_label = area_label + "-" + line_no

        self.filter = merge_filters(self.filter, {"labels.unit": [unit_label]})



@dataclass
class FishtalkBiomassCount(FishtalkAttribute):
  meta: Item = Item(
        name = "Biomasse antall",
        engUnit = "stk",
        visible = True,
  )
  def __post_init__(self):
        self.filter = merge_filters(self.filter, {"name": "fishtalkparser.Closing Count"})
        super().__post_init__()
```

### Reusable attributes example

```python
@dataclass
class ValveAeration(ScadaAttribute):
  meta: Item = Item(
        name = "Valve X",
        engUnit = "",
        valueType="enum",
        enumValues={
            "0": "Closed",
            "1": "Open"
        },
        visible = True,
  )
  def __post_init__(self):
    self.filter = merge_filters(self.filter, {"name": "Value"})
    super().__post_init__()



valve_aeration_list = [
    ValveAeration(name = f"Valve {i}", filter = {"labels.folder-3": [f"Valve_Aeriation_{i}"]})
    for i in range(1,9)
]
```

### Reusable attributes with different filters

```python
va = ValveAeration()

house = Asset(
    labels=[{"site":"home"}],
    attributes=[
        va.copy(
            name="Aeration Kitchen",
            add_filter={
                "labels.room": "Kitchen"
            }
        ),
        va.copy(
            name="Aeration Living room",
            add_filter={
                "labels.room": "Living room"
            }
        )
    ]
)
```
