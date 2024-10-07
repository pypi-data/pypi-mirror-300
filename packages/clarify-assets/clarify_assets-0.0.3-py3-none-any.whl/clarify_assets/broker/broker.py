import re
import tempfile
from time import sleep
from tqdm import tqdm

from pyclarify import Client
from pyclarify.experimental import ExperimentalClient
from pyclarify.fields.resource import (
    RelationshipsDictSignal,
    RelationshipDataToOne,
    Identifier,
)

from ..__utils__.parsers import (
    parse_filter,
    flatten,
    get_all_keys,
    parse_to_sqlite3,
    scuffed_filter_key_extraction,
)
from ..__utils__.validators import (
    get_item_id_or_none,
    compare_meta_and_published_item,
    can_be_published,
)
from ..__utils__.printing import color


def iterate_nodes(asset):
    leaves = []
    if asset.children:
        for child in asset.children:
            leaves += iterate_nodes(child)
    if asset.attributes:
        for attribute in asset.attributes:
            leaves += [attribute]
    return leaves


def make_query(filter, table="signals"):
    return f"SELECT HashKey from {table} WHERE " + parse_filter(filter)


class AssetBroker:
    def __init__(self, credentials, integrations):
        self.credentials = credentials
        self.INTEGRATIONS = integrations
        self.client = Client(credentials)
        self.exp_client = ExperimentalClient(credentials)
        self.SIGNALS = None
        self.ITEMS = None
        self.look_up_signals = None
        self.look_up_items = None
        self.SET_OF_SIGNAL_KEYS = None
        self.SET_OF_ITEM_KEYS = None
        self.con = None
        self.cur = None
        self.hash_map_signals = None
        self.hash_map_items = None

        self.tmp_folder = tempfile.TemporaryDirectory()
        self.tmp_folder_path = self.tmp_folder.name

    def get_data_from_clarify(self, reset=False):
        if not reset:
            if self.SIGNALS and self.ITEMS:
                return
        signals = []
        for integration in self.INTEGRATIONS:
            r = self.client.select_signals(
                integration=integration, limit=99999, include=["item"]
            )
            if r.error:
                num_errors = len(r.error)
            else:
                num_errors = 0
            if r.result:
                if r.result.data:
                    num_signals = len(r.result.data)
                    for s in r.result.data:
                        s.relationships.integration = RelationshipsDictSignal(
                            integration=RelationshipDataToOne(
                                data=Identifier(type="integration", id=integration)
                            )
                        )
                        signals += [s]
                else:
                    num_signals = 0
            else:
                print(r.error)
            print(
                f"Integration: {integration} - signals: {num_signals} - errors: {num_errors}"
            )
            sleep(0.5)

        self.SIGNALS = signals

        items = []

        r = self.client.select_items(limit=99999)
        items = r.result.data
        print(f"Retrieved {len(items)} items")

        self.ITEMS = items

        # POST PROCESS
        self.look_up_signals = [flatten(s) for s in self.SIGNALS]
        self.look_up_items = [flatten(i) for i in self.ITEMS]
        self.SET_OF_SIGNAL_KEYS = get_all_keys(self.look_up_signals)
        self.SET_OF_ITEM_KEYS = get_all_keys(self.look_up_items)

    def set_up_db(self):
        # check if already has db
        if self.con:
            import tempfile

            self.cur.close()
            self.con.close()
            self.tmp_folder.cleanup()
            self.tmp_folder = tempfile.TemporaryDirectory()
            self.tmp_folder_path = self.tmp_folder.name

        import sqlite3
        import uuid
        import hashlib

        con = sqlite3.connect(f"{self.tmp_folder_path}/{uuid.uuid4()}.db")
        print("Created SQLite3 db")
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS items;")
        cur.execute("DROP TABLE IF EXISTS signals;")
        # ADD REGEX FUNCTIONALITY

        def functionRegex(value, pattern):
            c_pattern = re.compile(r"\b" + pattern.lower() + r"\b")
            return c_pattern.search(value) is not None

        con.create_function("REGEXP", 2, functionRegex)

        cur.execute(
            f"CREATE TABLE items({', '.join(self.SET_OF_ITEM_KEYS).replace('-', '_')})"
        )
        cur.execute(
            f"CREATE TABLE signals({', '.join(self.SET_OF_SIGNAL_KEYS).replace('-', '_')})"
        )

        data = []
        hash_map_signals = {}
        for lus, s in zip(self.look_up_signals, self.SIGNALS):
            hash_key = hashlib.sha256(str(lus).encode("utf-8")).hexdigest()

            hash_map_signals[hash_key] = s
            data.append(parse_to_sqlite3(lus, self.SET_OF_SIGNAL_KEYS, hash_key))

        inputs = "?, " * len(self.SET_OF_SIGNAL_KEYS)
        inputs = inputs[:-2]
        cur.executemany(f"INSERT INTO signals VALUES ({inputs})", data)

        data = []
        hash_map_items = {}
        for lui, i in zip(self.look_up_items, self.ITEMS):
            hash_key = hashlib.sha256(str(lui).encode("utf-8")).hexdigest()

            hash_map_items[hash_key] = i
            data.append(parse_to_sqlite3(lui, self.SET_OF_ITEM_KEYS, hash_key))

        inputs = "?, " * len(self.SET_OF_ITEM_KEYS)
        inputs = inputs[:-2]
        cur.executemany(f"INSERT INTO items VALUES ({inputs})", data)

        con.commit()
        print("Finished inserting data")
        self.con = con
        self.cur = cur
        self.hash_map_signals = hash_map_signals
        self.hash_map_items = hash_map_items

    def flush_and_build_db(self, reset_clarify=False):
        self.get_data_from_clarify(reset_clarify)
        self.set_up_db()

    def is_valid_filter(self, filter, table):
        # Very Scuffed not happy
        valid_keys = getattr(self, f"SET_OF_{table.upper()[0:-1]}_KEYS")
        for k in scuffed_filter_key_extraction(filter):
            if k not in valid_keys:
                return False
        return True

    def query_sqlite(self, filter, table="signals"):
        if not self.is_valid_filter(filter, table):
            return []
        q = make_query(filter, table=table)

        res = self.cur.execute(q)
        return res.fetchall()

    def assign_signals(self, asset, force_reset=False):
        leaves = iterate_nodes(asset)
        if force_reset:
            for leaf in leaves:
                leaf.signals = []

        for leaf in tqdm(leaves, leave=True):
            if not force_reset:
                if leaf.signals:
                    continue
            hash_keys_ids = self.query_sqlite(leaf.filter)
            signals = []
            for hash_key_id in hash_keys_ids:
                hash_key_id = hash_key_id[0]
                signals.append(self.hash_map_signals[hash_key_id])
            if signals:
                leaf.add_signal(signals)

    def check_for_published_item(
        self, leaf, match_labels=["site", "area", "line", "cell", "data-source"]
    ):
        item = leaf.meta
        jattr = item.model_dump(mode="json")

        # Check necessary fields
        # Name, Area, maybe Line, maybe Cell
        and_list = [{"name": jattr["name"]}]
        for label in match_labels:
            if label in jattr["labels"].keys():
                and_list += [{f"labels.{label}": jattr["labels"][label]}]
        filt = {"$and": and_list}
        hash_keys_ids = self.query_sqlite(filt, "items")
        items = []
        for hash_key_id in hash_keys_ids:
            hash_key_id = hash_key_id[0]
            possible_items = self.hash_map_items[hash_key_id]
            if not isinstance(possible_items, list):
                items.append(possible_items)

        # Check self.signals
        possible_item_id = get_item_id_or_none(leaf)
        if possible_item_id:
            possible_item = list(
                filter(lambda i: possible_item_id == i.id, self.ITEMS)
            )[0]

            if possible_item not in items:
                items.append(possible_item)

        items = sorted(items, key=lambda i: i.meta.createdAt, reverse=True)

        return items

    def publish_leaves(self, leaves):
        for integration in self.INTEGRATIONS:
            sub_leaves = list(
                filter(
                    lambda x: (
                        x.signals[0].relationships.integration.integration.data.id
                        == integration
                        if x.signals
                        else False
                    ),
                    leaves,
                )
            )
            sub_leaves = {l.signals[0].id: l.meta for l in sub_leaves}
            r = self.client.publish_signals(
                items_by_signal=sub_leaves, integration=integration
            )
            print(r)

    def connect_signal_to_item(self, signal, item):
        source_signal_id = signal.id
        source_integration = signal.relationships.integration.integration.data.id

        print(f"connecting {source_signal_id} to {item.id}")
        r = self.exp_client.connect_signals(
            filter={
                "id": source_signal_id,
            },
            integration=source_integration,
            item=item.id,
            # include=["item"],
            dryrun=False,
        )

    def connect_leaves_to_items(self, old_leaves):
        for leaf, item in old_leaves:
            possible_item_id = get_item_id_or_none(leaf)
            if possible_item_id:
                if possible_item_id != item.id:
                    self.connect_signal_to_item(leaf.signals[0], item)
            else:
                self.connect_signal_to_item(leaf.signals[0], item)

    def disconnect_signal(self, signal):
        source_signal_id = signal.id
        source_integration = signal.relationships.integration.integration

        # disconnect from old item
        r = self.exp_client.disconnect_signals(
            filter={
                "id": source_signal_id,
            },
            integration=source_integration,
            dryrun=False,
        )

    def disconnect_and_reconnect(self, signal, new_item, old_item):
        source_signal = list(
            filter(
                lambda s: (
                    old_item.id in s.relationships.item.data.id
                    if s.relationships.item.data
                    else False
                ),
                self.SIGNALS,
            )
        )[0]
        source_signal_id = source_signal.id
        source_integration = source_signal.relationships.integration.integration.data.id
        self.disconnect_signal(source_signal)
        self.connect_signal_to_item(source_signal, new_item)

    def publish_asset(self, asset):
        leaves = iterate_nodes(asset)
        new_leaves = []
        old_leaves = []
        new_meta = []  # For future
        conflicting_leaves = []

        for leaf in leaves:
            if not can_be_published(leaf):
                continue

            # Check for existing items
            items = self.check_for_published_item(leaf)

            if items:
                if len(items) == 1:
                    possible_id = get_item_id_or_none(leaf)
                    if items[0].id == possible_id:
                        new_labels, removed_labels = compare_meta_and_published_item(
                            leaf, items[0]
                        )
                        if new_labels or removed_labels:
                            old_leaves.append((leaf, items[0]))
                    else:
                        old_leaves.append((leaf, items[0]))
                else:
                    conflicting_leaves.append((leaf, items))
            else:
                new_leaves.append(leaf)
        if new_leaves:
            print("New Items")
            print(f"{color.BOLD}{'Signal Name':30}{'Labels':60}{color.END}")
            for leaf in new_leaves:
                labels = list(map(lambda l: list(l.values())[0], leaf.labels))[::-1]
                print(f"{str(leaf):30}{' -> '.join(labels)}")

            ans = input("\nPublish signals? y/n \n")
            if ans == "y":
                print("Publishing all new signals")
                self.publish_leaves(new_leaves)
            else:
                print("You declined")

        print()
        if old_leaves:
            print("Signals with existing Item")
            print(
                f"{color.BOLD}{'Signal Name':30}{'Existing Id':30}{'Labels':40}{'Removed labels':50}{'New labels'}{color.END}"
            )
            for leaf, item in old_leaves:
                new_labels, removed_labels = compare_meta_and_published_item(leaf, item)

                new_labels_formatted = " | ".join(
                    [
                        f'{nl[0]}:{nl[-1] if nl[-1] else f"{color.RED}Null{color.END}"}'
                        for nl in new_labels
                    ]
                )
                removed_labels_formatted = " | ".join(
                    [f'{rl[0]}:{rl[-1] if rl[-1] else "Null"}' for rl in removed_labels]
                )

                labels = list(map(lambda l: list(l.values())[0], leaf.labels))[:2:][
                    ::-1
                ]
                curr_labels_formatted = " -> ".join(labels)
                print(
                    f"{str(leaf):30}{item.id:30}{curr_labels_formatted:40}{removed_labels_formatted:50}{new_labels_formatted}"
                )

            ans = input("\nConnect signal sources? y/n\n")
            if ans == "y":
                self.connect_leaves_to_items(old_leaves)
                ans = input("\nMerge(m) or overwrite(o) conflicting metas? m/o\n")
                if ans == "m":
                    ans = input("\nOld has precedence? y/n\n")
                    if ans == "y":
                        old_precedes = True
                    else:
                        old_precedes = False

                    for leaf, item in old_leaves:
                        new_labels, removed_labels = compare_meta_and_published_item(
                            leaf, item
                        )
                        preceded_label = new_labels if old_precedes else removed_labels
                        preceding_label = removed_labels if old_precedes else new_labels
                        updated_dict = dict(set(preceded_label) ^ set(preceding_label))
                        for k, v in updated_dict.items():
                            if k == "name":
                                leaf.meta.name = v
                            elif k == "engUnit":
                                leaf.meta.engUnit = v
                            else:
                                leaf.meta.labels[k] = [v]

                    self.publish_leaves([leaf for leaf, item in old_leaves])

                elif ans == "o":
                    self.publish_leaves([leaf for leaf, item in old_leaves])
            else:
                print("You declined")

        print()
        if conflicting_leaves:
            print("Conflicting Signals")
            print(
                f"{color.BOLD}{'Signal Name':30}{'Existing Id':30}{'Labels':40}{'Removed labels':50}{'New labels'}{color.END}"
            )
            for leaf, items in conflicting_leaves:
                for item in items:
                    new_labels, removed_labels = compare_meta_and_published_item(
                        leaf, item
                    )

                    new_labels_formatted = " | ".join(
                        [
                            f'{nl[0]}:{nl[-1] if nl[-1] else f"{color.RED}Null{color.END}"}'
                            for nl in new_labels
                        ]
                    )
                    removed_labels_formatted = " | ".join(
                        [
                            f'{rl[0]}:{rl[-1] if rl[-1] else "Null"}'
                            for rl in removed_labels
                        ]
                    )

                    labels = list(map(lambda l: list(l.values())[0], leaf.labels))[:2:][
                        ::-1
                    ]
                    curr_labels_formatted = " -> ".join(labels)
                    print(
                        f"{str(leaf):30}{item.id:30}{curr_labels_formatted:40}{removed_labels_formatted:50}{new_labels_formatted}"
                    )

            ans = input(
                "Disconnect signal from old item and connect to new item? y/n \n"
            )

            if ans == "y" and False:  # Skipping this for now
                print("Disconnecting and reconnecting signals")
                self.disconnect_and_reconnect(leaf.signals[0], item[0], item[1])
                print("Remember to delete/update old items!")
            else:
                print("you declined")
