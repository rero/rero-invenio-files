# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Thumbnail generation and full text extraction component."""

import contextlib
import os
import unicodedata
from io import BytesIO

import fitz
from flask import current_app
from invenio_records_resources.services.errors import FileKeyNotFoundError
from invenio_records_resources.services.files.components.base import (
    FileServiceComponent,
)
from PIL import Image


class ThumbnailAndFulltextComponent(FileServiceComponent):
    """Basic image metadata extractor."""

    @staticmethod
    def change_filename_extension(filename, extension):
        """Return filename with the given extension.

        Additionally, the original extension is appended to the filename, to avoid
        conflict with other files having the same name (without extension).
        """
        basename, ext = os.path.splitext(filename)

        if not basename:
            raise Exception(f"{filename} is not a valid filename")

        if not ext:
            return f"{basename}.{extension}"
        # remove dot
        ext = ext.replace(".", "")
        return f"{basename}-{ext}.{extension}"

    @staticmethod
    def create_thumbnail_from_file(file_path, mimetype):
        """Create a thumbnail from given file path and return image blob.

        :param file_path: Full path of file.
        :param mimetype: Mime type of the file.
        :returns: the binary data.
        """
        # Thumbnail can only be done from images or PDFs.
        if not mimetype.startswith("image/") and mimetype != "application/pdf":
            return None

        # For PDF, we take only the first page
        if mimetype == "application/pdf":
            max_width = max_height = 200
            with fitz.open(file_path) as pdf_document:
                page = pdf_document[0]
                scale_factor = min(max_width / page.rect.width, max_height / page.rect.height)
                # alpha=False avoids allocating an unused alpha channel
                pixmap = page.get_pixmap(matrix=fitz.Matrix(scale_factor, scale_factor), alpha=False)
                return pixmap.tobytes(output="jpg", jpg_quality=85)

        else:
            with Image.open(file_path) as img:
                # For palette images, convert before resizing to preserve transparency
                if img.mode == "P":
                    img = img.convert("RGBA")
                # Hint JPEG decoder to subsample during decode (1/2, 1/4, or 1/8)
                img.draft(None, (200, 200))
                # Resize first — color conversion then runs on 200px, not the original
                img.thumbnail((200, 200))
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert("RGB")
                buf = BytesIO()
                img.save(buf, format="JPEG", quality=85)
                return buf.getvalue()

    @staticmethod
    def create_fulltext_from_file(file_path, mimetype):
        """Extract the fulltext for a given pdf file.

        :param file_path: str - the path of the file.
        :param mimetype: str - the mime type of the file.
        :returns: the extracted text.
        :rtype: str
        """
        if mimetype != "application/pdf":
            return None
        flags = fitz.TEXTFLAGS_TEXT | fitz.TEXT_DEHYPHENATE
        with fitz.open(file_path) as pdf_file:
            if pdf_file.is_encrypted:
                return None
            pages = (
                unicodedata.normalize("NFKC", page.get_text("text", flags=flags, sort=True)).strip()
                for page in pdf_file
            )
            return "\n".join(t for t in pages if t) or None

    def commit_file(self, identity, id_, file_key, record):
        """Commit file handler.

        :param identity: flask principal Identity
        :param id_: str - record file id.
        :param file_key: str - file key in the file record.
        :param record: obj - record instance.
        """
        # already a thumbnail
        if record.files[file_key].get("metadata", {}).get("type") == "thumbnail":
            return
        rfile = record.files[file_key].file
        sf = self.service
        recid = record.pid.pid_value
        # thumbnail
        try:
            if blob := self.create_thumbnail_from_file(rfile.uri, rfile.mimetype):
                thumb_name = self.change_filename_extension(file_key, "jpg")
                sf.init_files(
                    identity=identity,
                    id_=recid,
                    data=[
                        {
                            "key": thumb_name,
                            "metadata": {
                                "type": "thumbnail",
                                "thumbnail_for": file_key,
                            },
                        }
                    ],
                    uow=self.uow,
                )
                sf.set_file_content(
                    identity,
                    id_=recid,
                    file_key=thumb_name,
                    stream=BytesIO(blob),
                    uow=self.uow,
                )
                sf.commit_file(identity=identity, id_=recid, file_key=thumb_name, uow=self.uow)
        except Exception:
            current_app.logger.debug("Thumbnail generation failed for %s", file_key, exc_info=True)
        # fulltext
        try:
            if fulltext := self.create_fulltext_from_file(rfile.uri, rfile.mimetype):
                thumb_name = self.change_filename_extension(file_key, "txt")
                sf.init_files(
                    identity=identity,
                    id_=recid,
                    data=[
                        {
                            "key": thumb_name,
                            "metadata": {
                                "type": "fulltext",
                                "fulltext_for": file_key,
                            },
                        }
                    ],
                    uow=self.uow,
                )
                sf.set_file_content(
                    identity=identity,
                    id_=recid,
                    file_key=thumb_name,
                    stream=BytesIO(fulltext.encode()),
                    uow=self.uow,
                )
                sf.commit_file(identity=identity, id_=recid, file_key=thumb_name, uow=self.uow)
        except Exception:
            current_app.logger.debug("Fulltext extraction failed for %s", file_key, exc_info=True)

    def delete_file(self, identity, id_, file_key, record, deleted_file):
        """Delete file handler.

        :param identity: flask principal Identity
        :param id_: str - record file id.
        :param file_key: str - file key in the file record.
        :param record: obj - record instance.
        :param deleted_file: file instance - the deleted file instance.
        """
        # a thumbnail or a fulltext
        if deleted_file.get("metadata", {}).get("type") in ["thumbnail", "fulltext"]:
            return
        sf = self.service
        recid = record.pid.pid_value
        thumb_name = self.change_filename_extension(file_key, "jpg")
        with contextlib.suppress(FileKeyNotFoundError):
            sf.delete_file(identity=identity, id_=recid, file_key=thumb_name, uow=self.uow)
        fulltext_name = self.change_filename_extension(file_key, "txt")
        with contextlib.suppress(FileKeyNotFoundError):
            sf.delete_file(identity=identity, id_=recid, file_key=fulltext_name, uow=self.uow)
