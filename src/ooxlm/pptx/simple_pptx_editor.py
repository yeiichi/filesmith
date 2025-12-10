# src/ooxlm/pptx/simple_pptx_editor.py

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from ooxlm.common.zip_ops import list_members, load_member, rewrite_zip

PathLike = str | Path

SLIDES_PREFIX = "ppt/slides/"
SLIDE_BASENAME = "slide"
SLIDE_EXT = ".xml"


class SimplePptxEditor:
    """
    Minimalistic PPTX text editor using Python stdlib only.

    Responsibilities:
      - Discover and load ppt/slides/slide*.xml from a .pptx file
      - Provide simple text extraction across all slides
      - Provide naive search & replace on text runs
      - Save a modified .pptx by rebuilding the ZIP container

    This is intentionally small: only slide XML is considered.
    No notes, masters, layouts, images, etc. (for now).
    """

    def __init__(self, path: PathLike):
        """
        Initialize editor from an existing PPTX file.

        Parameters
        ----------
        path : str | Path
            Path to the .pptx file.
        """
        self.path = Path(path)
        self._slides: dict[str, ET.Element] = {}
        self._load_slides()

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _load_slides(self) -> None:
        """
        Discover and parse all slide XML files.

        Slides are expected under:
            ppt/slides/slide1.xml, ppt/slides/slide2.xml, ...
        """
        if not self.path.is_file():
            raise FileNotFoundError(f"PPTX file not found: {self.path}")

        members = list_members(self.path)

        slide_names = sorted(
            name
            for name in members
            if name.startswith(SLIDES_PREFIX)
            and name[len(SLIDES_PREFIX):].startswith(SLIDE_BASENAME)
            and name.endswith(SLIDE_EXT)
        )

        if not slide_names:
            raise RuntimeError(f"No slide XMLs found in PPTX: {self.path}")

        slides: dict[str, ET.Element] = {}
        for name in slide_names:
            xml_bytes = load_member(self.path, name)
            try:
                root = ET.fromstring(xml_bytes)
            except ET.ParseError as exc:
                raise RuntimeError(
                    f"Failed to parse slide XML {name!r} in PPTX: {self.path}"
                ) from exc
            slides[name] = root

        self._slides = slides

    def _iter_text_nodes(self):
        """
        Iterate over all w:t nodes across all slides.
        """
        for root in self._slides.values():
            for node in root.iter():
                if node.tag.endswith("}t"):  # w:t
                    yield node

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def get_text(self, separator: str = " ") -> str:
        """
        Return concatenated text from all slides.

        Parameters
        ----------
        separator : str, optional
            String used to join individual text nodes. Defaults to " "
            for PPTX, as separate runs are often visually separated.

        Returns
        -------
        str
            Combined visible text (very naive; no layout awareness).
        """
        texts: list[str] = []
        for node in self._iter_text_nodes():
            if node.text:
                texts.append(node.text)
        return separator.join(texts)

    def replace(self, old: str, new: str) -> int:
        """
        Naively replace text in all w:t nodes across all slides.

        Parameters
        ----------
        old : str
            Substring to search for.
        new : str
            Replacement text.

        Returns
        -------
        int
            Number of text nodes that were modified (not total replacements).
        """
        if not old:
            return 0

        changed_nodes = 0
        for node in self._iter_text_nodes():
            if not node.text:
                continue
            new_text = node.text.replace(old, new)
            if new_text != node.text:
                node.text = new_text
                changed_nodes += 1
        return changed_nodes

    def save(self, output_path: PathLike) -> None:
        """
        Save the edited presentation to a new PPTX file.

        Parameters
        ----------
        output_path : str | Path
            Path where the new PPTX file will be written.

        Notes
        -----
        This rebuilds the PPTX ZIP archive, replacing only
        'ppt/slides/slide*.xml' and copying all other members as-is.
        """
        output_path = Path(output_path)

        replacements: dict[str, bytes] = {}
        for name, root in self._slides.items():
            replacements[name] = ET.tostring(
                root,
                encoding="utf-8",
                xml_declaration=True,
            )

        rewrite_zip(
            self.path,
            output_path,
            replacements=replacements,
        )
