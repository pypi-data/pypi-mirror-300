# Copyright (c) 2020 - Ashwin Vishnu <dev@fluid.quest>
# Copyright (c) 2016 - Mathieu Bridon <bochecha@daitauha.fr>
#
# This file is part of pelican-aio-planet
#
# pelican-aio-planet is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelican-aio-planet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pelican-aio-planet.  If not, see <http://www.gnu.org/licenses/>.

import bleach
from dateutil import parser as dtparser

from pelican.utils import truncate_html_words


def make_date(date_string):
    return dtparser.parse(date_string)


def make_summary(text, max_words=None):
    if max_words is None:
        return text

    text_truncated = truncate_html_words(text, max_words, end_text="…")

    tags = set(bleach.sanitizer.ALLOWED_TAGS) | {
        "p",
        "img",
        "video",
        "audio",
        "picture",
        "source",
        "div",
        "span",
        "pre",
    }
    attrs = bleach.sanitizer.ALLOWED_ATTRIBUTES
    attrs.update(
        {tag: ["src", "alt", "title"] for tag in ("img", "video", "audio")}
    )
    attrs.update({"source": ["src", "srcset", "type"]})

    text_truncated_sanitized = bleach.clean(
        text_truncated,
        tags=tags,
        attributes=attrs,
        strip=True,
        strip_comments=True,
    )

    return text_truncated_sanitized
