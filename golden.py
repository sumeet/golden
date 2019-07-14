#!/usr/bin/env python3
import json
import sys
import pprint
import subprocess

GOLDEN = (1 + 5 ** 0.5) / 2
GOLDEN_RATIO = 1 / GOLDEN
GOLDEN_RATIO_INVERSE = 1 - GOLDEN_RATIO


def query_current_desktop():
    result = subprocess.run(['bspc', 'query', '-T', '-n', '@/'],
                            stdout=subprocess.PIPE)
    return Node(json.loads(result.stdout))


def set_node_ratio(node_id, ratio):
    subprocess.run(['bspc', 'node', str(node_id), '-r', str(ratio)])


class Node:

    def __init__(self, raw_output, parent=None):
        self._raw_output = raw_output
        self.parent = parent

    @property
    def is_private(self):
        return self._raw_output['private']

    @property
    def id(self):
        return self._raw_output['id']

    @property
    def first_child(self):
        if self._raw_output['firstChild']:
            return Node(self._raw_output['firstChild'], parent=self)
        return None

    @property
    def second_child(self):
        if self._raw_output['secondChild']:
            return Node(self._raw_output['secondChild'], parent=self)
        return None

    @property
    def all_children(self):
        first_child = self.first_child
        if first_child:
            yield first_child
            for child in first_child.all_children:
                yield child

        second_child = self.second_child
        if second_child:
            yield second_child
            for child in second_child.all_children:
                yield child

    def find_node(self, node_id):
        if self.id == node_id:
            return self
        if self.first_child:
            node = self.first_child.find_node(node_id)
            if node:
                return node
        if self.second_child:
            node = self.second_child.find_node(node_id)
            if node:
                return node


def enlarge_by_golden_ratio(node):
    parent = node.parent

    if not parent:
        return

    # don't resize if either child contains a window marked as private: that
    # means the user wants to keep this window from changing position or size
    # if possible
    if any(child.is_private for child in parent.all_children):
        return

    # in bspwm, nodes each have two children:
    #
    # if the node we're trying to enlarge is the first parent, then set the
    # node's ratio to the golden ratio. that will make it larger than the second
    # node. otherwise, set the ratio to the inverse of the golden ratio, and
    # then the second child (our node) will appear larger than the first child
    if parent.first_child.id == node.id:
        ratio = GOLDEN_RATIO
    if parent.second_child.id == node.id:
        ratio = GOLDEN_RATIO_INVERSE

    set_node_ratio(parent.id, ratio)
    enlarge_by_golden_ratio(parent)


def parse_node_focus_event(line):
    if not line.startswith('node_focus'):
        return None

    _, monitor_id, desktop_id, node_id = line.split()
    return int(monitor_id, 16), int(desktop_id, 16), int(node_id, 16)


if __name__ == '__main__':
    node_focus_events = filter(None, map(parse_node_focus_event, sys.stdin))


    for monitor_id, desktop_id, focused_node_id in node_focus_events:
        current_desktop_node = query_current_desktop()

        focused_node = current_desktop_node.find_node(focused_node_id)
        enlarge_by_golden_ratio(focused_node)
