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


from pathlib import Path

from pelican import signals
from pelican.generators import PagesGenerator

from .planet import Planet
from ._version import __version__  # noqa


def generate(generator):
    if not isinstance(generator, PagesGenerator):
        return

    config = generator.context

    feeds = config["PLANET_FEEDS"]
    max_articles_per_feed = config.get("PLANET_MAX_ARTICLES_PER_FEED", None)
    max_articles = config.get("PLANET_MAX_ARTICLES", 20)
    max_summary_length = config.get("PLANET_MAX_SUMMARY_LENGTH", None)
    max_age_in_days = config.get("PLANET_MAX_AGE_IN_DAYS", 180)
    resolve_redirects = config.get("PLANET_RESOLVE_REDIRECTS", False)
    template = Path(config["PLANET_TEMPLATE"])
    destination = Path(config["PLANET_PAGE"])

    planet = Planet(
        feeds,
        max_articles_per_feed=max_articles_per_feed,
        max_summary_length=max_summary_length,
        max_age_in_days=max_age_in_days,
        resolve_redirects=resolve_redirects,
    )
    planet.get_feeds()
    planet.write_page(template, destination, max_articles=max_articles)


def register():
    signals.generator_init.connect(generate)
