from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import List, Set, Optional, Tuple, Union

from .constants import PIPE, SPACER_PREFIX, ELBOW, TEE, SPACER
from .fictusfilesystem import FictusFileSystem
from .fictusnode import Folder, Node, File
from .renderer import Renderer, defaultRenderer, RenderTagEnum

pattern = re.compile(r"[^\\]")


class FictusDisplay:
    def __init__(self, ffs: FictusFileSystem):
        self._ffs = ffs
        self._renderer = defaultRenderer
        self._ignore: Set[int] = set()

    @property
    def renderer(self) -> Renderer:
        return self._renderer

    @renderer.setter
    def renderer(self, renderer: Renderer) -> None:
        self._renderer = renderer

    def _wrap_node_name_with_tags(self, node: Node):
        # setup defaults
        key = RenderTagEnum.FILE

        # account for the distinction between root and all other folders
        if isinstance(node, Folder):
            if node == self._ffs.root():
                key = RenderTagEnum.ROOT
            else:
                key = RenderTagEnum.FOLDER

        tags = self.renderer.tags(key)

        return f"{tags.open}{node.value}{tags.close}"

    def _display_node(self, node: Node, last: bool, node_level_start: int) -> str:
        """
        Bookkeeping of nested node depth, node siblings, and order in the queue are
        used to present the FicusSystem in an aesthetic way.
        """

        parts = [PIPE + SPACER_PREFIX for _ in range(node_level_start, node.height)]
        for index in self._ignore:
            if 0 < len(parts) > index - 1:
                parts[index - 1] = SPACER + SPACER_PREFIX

        if parts:
            parts[-1] = ELBOW if last is True else TEE

        return f'{"".join(parts)}{self._wrap_node_name_with_tags(node)}'

    @staticmethod
    def _custom_sort(nodes: List[Node]) -> List[Node]:
        """Reverse sort the children by file, then name."""
        return sorted(nodes, key=lambda x: (isinstance(x, File), x.value.lower()), reverse=True)

    def pprint(self, renderer: Optional[Renderer] = None) -> None:
        """Displays the file system structure to stdout."""

        old_renderer, self._renderer = self._renderer, renderer or self._renderer

        node_start = self._ffs.current()

        node_level_start = node_start.height

        self._ignore = set(range(node_start.height))

        prefix: int = -1  # not set

        buffer: List[str] = []

        q: List[Tuple[Node, bool]] = [(node_start, True)]
        while q:
            node, last = q.pop()
            if last is False:
                if node.height in self._ignore:
                    self._ignore.remove(node.height)
            line: str = self._display_node(node, last, node_level_start)

            # This needs to happen only once and applied
            # thereafter to each subsequent line.
            prefix = len(line) - len(line.lstrip()) if prefix == -1 else prefix

            buffer.append(f"{line[prefix:]}\n")
            if last is True:
                # track nodes without children.
                self._ignore.add(node.height)

            if isinstance(node, Folder) and node.children:
                children = self._custom_sort(node.children)
                sorted_children = [(child, False) for child in children]
                c, _ = sorted_children[0]
                sorted_children[0] = (c, True)

                q += sorted_children

        # output data
        sys.stdout.write(self._renderer.tags(RenderTagEnum.DOC).open)
        sys.stdout.writelines(buffer)
        sys.stdout.write(self._renderer.tags(RenderTagEnum.DOC).close)

        # reset renderer to what it was
        self._renderer = old_renderer

    # Reforestation methods - - - - - - -
    @staticmethod
    def _reforestation_path(node) -> str:
        parts = []
        while node:
            parts.append(node.value)
            node = node.parent
        return '//'.join(reversed(parts))

    def reforestation(self, path: Path) -> None:
        """
        Take the Fictus File System and generate the structure on disk using the path
        passed in as the root.
        """
        node_start = self._ffs.current()
        q: List[Tuple[Node, bool]] = [(node_start, True)]
        while q:
            node, last = q.pop()
            if last is False:
                if node.height in self._ignore:
                    self._ignore.remove(node.height)

            real_path = path / self._reforestation_path(node)
            if isinstance(node, Folder):
                real_path.mkdir(parents=True, exist_ok=True)
            else:
                with real_path.open("w", encoding="utf-8") as f:
                    f.write('')

            if isinstance(node, Folder):
                children = self._custom_sort(node.children)

                sorted_children = [(child, False) for child in children]
                if sorted_children:
                    c, _ = sorted_children[0]
                    sorted_children[0] = (c, True)

                q += sorted_children
