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

"""Module tests."""

from io import BytesIO
from unittest import mock

import fitz
from flask import Flask
from PIL import Image

from rero_invenio_files import REROInvenioFiles
from rero_invenio_files.records.components import ThumbnailAndFulltextComponent


def test_version():
    """Test version import."""
    from rero_invenio_files import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = REROInvenioFiles(app)
    assert "rero-invenio-files" in app.extensions

    app = Flask("testapp")
    ext = REROInvenioFiles()
    assert "rero-invenio-files" not in app.extensions
    ext.init_app(app)
    assert "rero-invenio-files" in app.extensions


def _jpeg_size(data):
    """Return (width, height) of a JPEG blob."""
    with Image.open(BytesIO(data)) as img:
        return img.size


# ---------------------------------------------------------------------------
# create_thumbnail_from_file unit tests
# ---------------------------------------------------------------------------


def test_thumbnail_unsupported_mimetype():
    """Return None for mimetypes that cannot produce a thumbnail."""
    assert ThumbnailAndFulltextComponent.create_thumbnail_from_file("irrelevant.docx", "application/msword") is None
    assert ThumbnailAndFulltextComponent.create_thumbnail_from_file("irrelevant.mp3", "audio/mpeg") is None


def test_thumbnail_pdf(tmp_path):
    """PDF thumbnail is a valid JPEG at most 200px on either dimension."""
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4
    page.insert_text((72, 72), "Test PDF thumbnail")
    doc.save(str(pdf_path))
    doc.close()

    result = ThumbnailAndFulltextComponent.create_thumbnail_from_file(str(pdf_path), "application/pdf")

    assert result is not None
    w, h = _jpeg_size(result)
    assert w <= 200
    assert h <= 200


def test_thumbnail_jpeg_rgb(tmp_path):
    """JPEG thumbnail is a valid JPEG at most 200px on either dimension."""
    img_path = tmp_path / "photo.jpg"
    img = Image.new("RGB", (1000, 800), color=(100, 150, 200))
    img.save(str(img_path), format="JPEG")

    result = ThumbnailAndFulltextComponent.create_thumbnail_from_file(str(img_path), "image/jpeg")

    assert result is not None
    w, h = _jpeg_size(result)
    assert w <= 200
    assert h <= 200


def test_thumbnail_png_with_alpha(tmp_path):
    """PNG with transparency is composited onto white and returned as JPEG."""
    img_path = tmp_path / "transparent.png"
    img = Image.new("RGBA", (400, 300), color=(0, 128, 255, 128))
    img.save(str(img_path), format="PNG")

    result = ThumbnailAndFulltextComponent.create_thumbnail_from_file(str(img_path), "image/png")

    assert result is not None
    # Must be a valid JPEG (no exception on open)
    with Image.open(BytesIO(result)) as out:
        assert out.format == "JPEG"
        assert out.mode == "RGB"
    w, h = _jpeg_size(result)
    assert w <= 200
    assert h <= 200


def test_thumbnail_png_rgb(tmp_path):
    """Opaque PNG is returned as a valid JPEG thumbnail."""
    img_path = tmp_path / "opaque.png"
    img = Image.new("RGB", (500, 500), color=(200, 100, 50))
    img.save(str(img_path), format="PNG")

    result = ThumbnailAndFulltextComponent.create_thumbnail_from_file(str(img_path), "image/png")

    assert result is not None
    w, h = _jpeg_size(result)
    assert w <= 200
    assert h <= 200


def test_thumbnail_palette_image(tmp_path):
    """Palette (P-mode) image with transparency is handled correctly."""
    img_path = tmp_path / "palette.png"
    img = Image.new("RGBA", (300, 300), color=(0, 255, 0, 200))
    img = img.convert("P")
    img.save(str(img_path), format="PNG")

    result = ThumbnailAndFulltextComponent.create_thumbnail_from_file(str(img_path), "image/png")

    assert result is not None
    with Image.open(BytesIO(result)) as out:
        assert out.format == "JPEG"
        assert out.mode == "RGB"


def test_thumbnail_portrait_fits_within_200(tmp_path):
    """Tall portrait image: width stays ≤200 and height stays ≤200."""
    img_path = tmp_path / "portrait.jpg"
    img = Image.new("RGB", (200, 2000), color=(10, 20, 30))
    img.save(str(img_path), format="JPEG")

    result = ThumbnailAndFulltextComponent.create_thumbnail_from_file(str(img_path), "image/jpeg")

    w, h = _jpeg_size(result)
    assert w <= 200
    assert h <= 200


# ---------------------------------------------------------------------------
# create_fulltext_from_file unit tests
# ---------------------------------------------------------------------------


def test_fulltext_unsupported_mimetype():
    """Return None for mimetypes that are not PDF."""
    assert ThumbnailAndFulltextComponent.create_fulltext_from_file("irrelevant.png", "image/png") is None
    assert ThumbnailAndFulltextComponent.create_fulltext_from_file("irrelevant.docx", "application/msword") is None


def test_fulltext_pdf(tmp_path):
    """PDF with extractable text returns the text content."""
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello World")
    doc.save(str(pdf_path))
    doc.close()

    result = ThumbnailAndFulltextComponent.create_fulltext_from_file(str(pdf_path), "application/pdf")

    assert isinstance(result, str)
    assert "Hello World" in result


def test_fulltext_empty_pdf_returns_none(tmp_path):
    """PDF with no text on any page returns None."""
    pdf_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()

    result = ThumbnailAndFulltextComponent.create_fulltext_from_file(str(pdf_path), "application/pdf")

    assert result is None


def test_fulltext_encrypted_pdf_returns_none(tmp_path):
    """Encrypted PDF returns None without raising."""
    pdf_path = tmp_path / "encrypted.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Secret content")
    doc.save(str(pdf_path), encryption=fitz.PDF_ENCRYPT_AES_256, user_pw="secret")
    doc.close()

    result = ThumbnailAndFulltextComponent.create_fulltext_from_file(str(pdf_path), "application/pdf")

    assert result is None


def test_fulltext_ligatures_normalised():
    """Ligatures are decomposed via NFKC normalisation (ﬁ → fi, ﬂ → fl)."""
    mock_page = mock.MagicMock()
    mock_page.get_text.return_value = "ﬁnd ﬂow"
    mock_doc = mock.MagicMock()
    mock_doc.__enter__ = mock.MagicMock(return_value=mock_doc)
    mock_doc.__exit__ = mock.MagicMock(return_value=False)
    mock_doc.is_encrypted = False
    mock_doc.__iter__ = mock.MagicMock(return_value=iter([mock_page]))

    with mock.patch("fitz.open", return_value=mock_doc):
        result = ThumbnailAndFulltextComponent.create_fulltext_from_file("dummy.pdf", "application/pdf")

    assert result == "find flow"


# ---------------------------------------------------------------------------


def test_files_api_flow(app, client, headers, file_location, pdf_file):
    """Test record creation."""
    # Initialize a draft
    data = {
        "collections": ["col1", "col2"],
        # links=[{"$ref": "https://localhost:5000/api/records/1"}],
        # owner={"$ref": "https://localhost:5000/api/users/1"},
    }
    res = client.post("/api/records", headers=headers, json={"metadata": data})
    assert res.status_code == 201
    id_ = res.json["id"]
    assert res.json["links"]["self"].endswith(f"/api/records/{id_}")
    data["collections"] = ["new col"]
    res = client.put(f"/api/records/{id_}", headers=headers, json={"metadata": data})
    assert res.status_code == 200
    assert res.json["metadata"]["collections"] == ["new col"]

    # Initialize files upload
    res = client.post(
        f"/api/records/{id_}/files",
        headers=headers,
        json=[{"key": "test.pdf", "metadata": {"label": "label1"}}],
    )
    assert res.status_code == 201
    res_file = res.json["entries"][0]
    assert res_file["key"] == "test.pdf"
    assert res_file["status"] == "pending"
    assert res_file["metadata"] == {"label": "label1"}
    assert res_file["links"]["self"].endswith(f"/api/records/{id_}/files/test.pdf")
    assert res_file["links"]["content"].endswith(f"/api/records/{id_}/files/test.pdf/content")
    assert res_file["links"]["commit"].endswith(f"/api/records/{id_}/files/test.pdf/commit")

    # Get the file metadata

    res = client.get(f"/api/records/{id_}/files/test.pdf", headers=headers)
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "pending"
    assert res.json["metadata"] == {"label": "label1"}

    # Upload a file
    res = client.put(
        f"/api/records/{id_}/files/test.pdf/content",
        headers={
            "content-type": "application/octet-stream",
            "accept": "application/json",
        },
        data=BytesIO(pdf_file),
    )
    assert res.status_code == 200
    assert res.json["status"] == "pending"

    # Commit the uploaded file
    res = client.post(f"/api/records/{id_}/files/test.pdf/commit", headers=headers)
    assert res.status_code == 200
    assert res.json["status"] == "completed"

    # Get the file metadata
    res = client.get(f"/api/records/{id_}/files/test.pdf", headers=headers)
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "completed"
    assert res.json["metadata"] == {"label": "label1"}
    # file_size = str(res.json["size"])
    assert set(res.json["links"].keys()) == {
        "self",
        "content",
        "commit",
        "preview",
        "thumbnail",
    }

    assert isinstance(res.json["size"], int), "File size not integer"

    # Read a file's content
    res = client.get(f"/api/records/{id_}/files/test.pdf/content", headers=headers)
    assert res.status_code == 200
    assert res.data == pdf_file

    res = client.get(f"/api/records/{id_}/files/test-pdf.jpg/content", headers=headers)
    assert res.status_code == 200

    # Test preview
    # Note: url_for works only on the top of the test
    with mock.patch("invenio_theme.views.render_template"):
        res = client.get("/records/foo/preview/test.pdf", headers=headers)
        assert res.status_code == 404
        res = client.get(f"/records/{id_}/preview/test1.pdf", headers=headers)
        assert res.status_code == 404
    with mock.patch("invenio_previewer.extensions.pdfjs.render_template"):
        res = client.get(f"/records/{id_}/preview/test.pdf", headers=headers)
        assert res.status_code == 200

    res = client.get(f"/api/records/{id_}/files/test-pdf.txt/content", headers=headers)
    assert res.status_code == 200
    assert "Title" in res.text

    # Update file metadata
    res = client.put(
        f"/api/records/{id_}/files/test.pdf",
        headers=headers,
        json={"metadata": {"title": "New title"}},
    )
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "completed"
    assert res.json["metadata"] == {"title": "New title"}

    # Get all files
    res = client.get(f"/api/records/{id_}/files", headers=headers)
    assert res.status_code == 200
    assert len(res.json["entries"]) == 3
    main_file = next(
        file for file in res.json["entries"] if file.get("metadata", {}).get("type") not in ["thumbnail", "fulltext"]
    )
    assert main_file["key"] == "test.pdf"
    assert main_file["status"] == "completed"
    assert main_file["metadata"] == {"title": "New title"}

    # Delete a file
    res = client.delete(f"/api/records/{id_}/files/test.pdf", headers=headers)
    assert res.status_code == 204

    # Get all files
    res = client.get(f"/api/records/{id_}/files", headers=headers)
    assert res.status_code == 200
    assert len(res.json["entries"]) == 0
