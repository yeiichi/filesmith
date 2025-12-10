# src/ooxlm/docx/simple_docx_editor.py

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from ooxlm.common.zip_ops import load_member, rewrite_zip

PathLike = str | Path

DOCUMENT_XML = "word/document.xml"


class SimpleDocxEditor:
    """
    Minimalistic DOCX text editor using Python stdlib only.

    Responsibilities:
      - Load word/document.xml from a .docx file
      - Provide simple text extraction
      - Provide naive search & replace on text runs
      - Save a modified .docx by rebuilding the ZIP container

    This is intentionally small and conservative: no styles, no images,
    no headers/footers (yet). It is meant as a foundation to grow on.
    """

    def __init__(self, path: PathLike):
        """
        Initialize editor from an existing DOCX file.

        Parameters
        ----------
        path : str | Path
            Path to the .docx file.
        """
        self.path = Path(path)
        self._xml_root = self._load_document_xml()

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _load_document_xml(self) -> ET.Element:
        """
        Load and parse word/document.xml from the DOCX file.

        Returns
        -------
        xml.etree.ElementTree.Element
            Root element of the document.xml tree.

        Raises
        ------
        FileNotFoundError
            If the DOCX file does not exist.
        RuntimeError
            If word/document.xml is missing or invalid.
        """
        if not self.path.is_file():
            raise FileNotFoundError(f"DOCX file not found: {self.path}")

        try:
            xml_bytes = load_member(self.path, DOCUMENT_XML)
        except KeyError as exc:
            raise RuntimeError(
                f"{DOCUMENT_XML!r} not found in DOCX archive: {self.path}"
            ) from exc

        try:
            return ET.fromstring(xml_bytes)
        except ET.ParseError as exc:
            raise RuntimeError(
                f"Failed to parse {DOCUMENT_XML!r} from DOCX: {self.path}"
            ) from exc

    def _iter_text_nodes(self):
        """
        Iterate over all w:t nodes in the document.

        This keeps namespace handling extremely simple by checking
        tag suffixes only ('.endswith(\"}t\")'), which works because
        DOCX uses qualified names like '{namespace}t' for w:t.
        """
        for node in self._xml_root.iter():
            if node.tag.endswith("}t"):  # w:t
                yield node

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def get_text(self, separator: str = "") -> str:
        """
        Return concatenated text from all text nodes in the document.

        Parameters
        ----------
        separator : str, optional
            String used to join individual text nodes. Defaults to "".

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
        Naively replace text in all w:t nodes.

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

        Notes
        -----
        - This is a simple string replace on each w:t node's .text.
        - It does not handle cross-node matches or regex.
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
        Save the edited document to a new DOCX file.

        Parameters
        ----------
        output_path : str | Path
            Path where the new DOCX file will be written.

        Notes
        -----
        This rebuilds the DOCX ZIP archive, replacing only
        'word/document.xml' and copying all other members as-is.
        """
        output_path = Path(output_path)

        # Serialize updated XML tree
        new_xml_bytes = ET.tostring(
            self._xml_root,
            encoding="utf-8",
            xml_declaration=True,
        )

        # Rebuild DOCX using the shared ZIP helper
        rewrite_zip(
            self.path,
            output_path,
            replacements={DOCUMENT_XML: new_xml_bytes},
        )
