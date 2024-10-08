# Copyright Jiaqi (Hutao of Emberfire)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest

import yaml

from wilhelm_python_sdk.german_neo4j_loader import get_attributes
from wilhelm_python_sdk.german_neo4j_loader import update_link_hints

UNKOWN_DECLENSION_NOUN_YAML = """
    term: die Grilltomate
    definition: the grilled tomato
    declension: Unknown
"""

HUT_YAML = """
    term: der Hut
    definition: the hat
    declension:
      - ["",         singular, singular, singular,      plural, plural]
      - ["",         indef.,   def.,     noun,          def.,   noun  ]
      - [nominative, ein,      der,      Hut,           die,    Hüte  ]
      - [genitive,   eines,    des,      "Hutes, Huts", der,    Hüte  ]
      - [dative,     einem,    dem,      Hut,           den,    Hüten ]
      - [accusative, einen,    den,      Hut,           die,    Hüte  ]
"""

HUT_DECLENSION_MAP = {
    "declension-0-0": "",
    "declension-0-1": "singular",
    "declension-0-2": "singular",
    "declension-0-3": "singular",
    "declension-0-4": "plural",
    "declension-0-5": "plural",

    "declension-1-0": "",
    "declension-1-1": "indef.",
    "declension-1-2": "def.",
    "declension-1-3": "noun",
    "declension-1-4": "def.",
    "declension-1-5": "noun",

    "declension-2-0": "nominative",
    "declension-2-1": "ein",
    "declension-2-2": "der",
    "declension-2-3": "Hut",
    "declension-2-4": "die",
    "declension-2-5": "Hüte",

    "declension-3-0": "genitive",
    "declension-3-1": "eines",
    "declension-3-2": "des",
    "declension-3-3": "Hutes, Huts",
    "declension-3-4": "der",
    "declension-3-5": "Hüte",

    "declension-4-0": "dative",
    "declension-4-1": "einem",
    "declension-4-2": "dem",
    "declension-4-3": "Hut",
    "declension-4-4": "den",
    "declension-4-5": "Hüten",

    "declension-5-0": "accusative",
    "declension-5-1": "einen",
    "declension-5-2": "den",
    "declension-5-3": "Hut",
    "declension-5-4": "die",
    "declension-5-5": "Hüte"

    # "declension": {
    #     0: {0: "",           1: "singular", 2: "singular", 3: "singular",    4: "plural", 5: "plural"},
    #     1: {0: "",           1: "indef.",   2: "def.",     3: "noun",        4: "def.",   5: "noun"},
    #     2: {0: "nominative", 1: "ein",      2: "der",      3: "Hut",         4: "die",    5: "Hüte"},
    #     3: {0: "genitive",   1: "eines",    2: "des",      3: "Hutes, Huts", 4: "der",    5: "Hüte"},
    #     4: {0: "dative",     1: "einem",    2: "dem",      3: "Hut",         4: "den",    5: "Hüten"},
    #     5: {0: "accusative", 1: "einen",    2: "den",      3: "Hut",         4: "die",    5: "Hüte"}
    # }
}


class TestGermanNeo4JLoader(unittest.TestCase):

    def test_get_attributes(self):
        self.assertEqual(
            {"name": "der Hut", "language": "German"} | HUT_DECLENSION_MAP,
            get_attributes(yaml.safe_load(HUT_YAML)),
        )

    def test_update_link_hints(self):
        self.assertEqual(
            {"Reis": "der Reis", "Reise": "der Reis"},
            update_link_hints({}, {"declension-1-1": "Reis", "declension-1-2": "Reise"}, "der Reis")
        )
