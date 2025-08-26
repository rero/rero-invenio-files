# RERO-Invenio-Files
# Copyright (C) 2024 RERO.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Test PDF Generator."""

import pytest
from PIL import Image

from rero_invenio_files.pdf import PDFGenerator


def test_pdf_generation(simple_data):
    """Test the pdf generation with standard data."""
    pdf = PDFGenerator(simple_data)
    pdf.render()
    assert pdf.pages_count == 1
    output = pdf.output(dest='S')
    assert isinstance(output, (bytes, bytearray))
    assert len(output) > 100


def test_pdf_generation_empty():
    """Test PDF generation when data is empty."""
    pdf = PDFGenerator({})
    pdf.render()
    assert pdf.pages_count == 1
    output = pdf.output(dest='S')
    assert isinstance(output, (bytes, bytearray))
    assert len(output) > 100



def test_header_footer_called(simple_data):
    """Test that header and footer are called during render using a subclass."""
    called = {"header": False, "footer": False}

    class TestPDF(PDFGenerator):
        def header(self):
            called["header"] = True

        def footer(self):
            called["footer"] = True

        def image(self, *a, **k):
            return None

    pdf = TestPDF(simple_data)
    pdf.add_page()  # force header/footer calls
    pdf.render()

    assert called["header"], "header() was not called"
    assert called["footer"], "footer() was not called"


def test_select_random_file(tmp_path):
    """Test _select_random_file for empty and non-empty folders."""
    folder = tmp_path / "logos"
    folder.mkdir()
    pdf = PDFGenerator({})

    # Empty folder
    assert pdf._select_random_file(folder, [".png"]) is None

    # Add a file
    file_path = folder / "logo.png"
    file_path.write_text("dummy")
    selected = pdf._select_random_file(folder, [".png"])
    assert selected == str(file_path)


def test_add_paragraph_fixed_height(simple_data):
    """Test _add_paragraph_fixed_height moves Y correctly."""
    pdf = PDFGenerator(simple_data)
    pdf.add_page()
    pdf._add_paragraph_fixed_height(max_height=50, top_padding=5)
    assert pdf.get_y() >= 50


def test_add_graphic_fixed_bottom(tmp_path, monkeypatch):
    """Test _add_graphic_fixed_bottom with and without an image file."""
    pdf = PDFGenerator({})
    pdf.add_page()

    # No file → should do nothing
    pdf.graph_path = str(tmp_path / "missing.png")
    assert pdf._add_graphic_fixed_bottom() is None

    # Create dummy image
    img_path = tmp_path / "graph.png"
    Image.new("RGB", (100, 50)).save(img_path)
    pdf.graph_path = str(img_path)

    # Track that image() is called
    called = {}

    def fake_image(*args, **kwargs):
        called['yes'] = True

    monkeypatch.setattr(pdf, "image", fake_image)

    # Call the method
    pdf._add_graphic_fixed_bottom()

    # Assert that image method was called
    assert called.get('yes') is True

