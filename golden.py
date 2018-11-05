#!/usr/bin/env python3
import json
import sys
import pprint
import subprocess


GOLDEN = (1 + 5 ** 0.5) / 2
GOLDEN_FIRST = 1 / GOLDEN
GOLDEN_SECOND = 1 - GOLDEN_FIRST


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
    if not node.parent:
        return
    if node.parent.first_child.id == node.id:
        ratio = GOLDEN_FIRST
    if node.parent.second_child.id == node.id:
        ratio = GOLDEN_SECOND
    set_node_ratio(node.parent.id, ratio)
    enlarge_by_golden_ratio(node.parent)


def parse_node_focus_event(line):
    if not line.startswith('node_focus'):
        return None

    _, monitor_id, desktop_id, node_id = line.split()
    return int(monitor_id, 16), int(desktop_id, 16), int(node_id, 16)


node_focus_events = filter(None, map(parse_node_focus_event, sys.stdin))


for monitor_id, desktop_id, focused_node_id in node_focus_events:
    current_desktop_node = query_current_desktop()

    focused_node = current_desktop_node.find_node(focused_node_id)
    enlarge_by_golden_ratio(focused_node)
