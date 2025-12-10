# ooxlm – OOXML Simple Editor (internal)

> **Status:** Experimental, internal module under the `filesmith` project.  
> Public API and packaging are **not** stable yet.

`ooxlm` provides a minimal, stdlib-only toolkit for working with OOXML
documents (DOCX / PPTX):

- `ooxlm.common.zip_ops` – small helpers for reading and rewriting ZIP-based OOXML files
- `ooxlm.docx.SimpleDocxEditor` – naïve DOCX text extractor / search & replace
- `ooxlm.pptx.SimplePptxEditor` – naïve PPTX text extractor / search & replace

## Design goals

- **Stdlib only** – no `python-docx`, no `lxml`
- **Small and inspectable** – focus on learning and controlled editing
- **Tested** – comes with pytest coverage for the core primitives

## Usage (internal)

Typical internal usage within this repo looks like:

```python
from ooxlm.docx import SimpleDocxEditor
from ooxlm.pptx import SimplePptxEditor

doc = SimpleDocxEditor("input.docx")
doc.replace("foo", "bar")
doc.save("output.docx")

ppt = SimplePptxEditor("input.pptx")
print(ppt.get_text())
