# Utility functions for making sigular or plural forms of nouns

# Copyright 2018 Nicko van Someren
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

# SPDX-License-Identifier: Apache-2.0

import locale

# Paterns for converting singluar to plural forms.
# Each set is a list of tuples of ([suffix set], chop, plural_suffix)
# where the 'chop' flag indicates if the matched sinular suffix should be
# removed. Matching is done in order or occurance so the default ("" suffix)
# must come last

_plural_patterns = {
# English set:
    "en": [
        (["s", "sh", "ch", "x", "o"], False, "es"),
        (["ay", "ey", "iy", "oy", "uy"], False, "s"),
        (["y"], True, "ies"),
        (["f", "fe"], True, "ves"),
        ([""], False, "s")
        ]
    }

# Default to English, because I'm British!
_default_locale = "en"

class Plurality:
    def __init__(self, locale_name=_default_locale):
        if locale_name in _plural_patterns:
            self.patterns = _plural_patterns[locale_name]
        elif locale_name.split("_")[0] in _plural_patterns:
            locale_name = locale_name.split("_")[0]
            self.patterns = _plural_patterns[locale_name]
        else:
            self.patterns = _plural_patterns[_default_locale]

    def singular(self, word):
        if '|' in word:
            stem, s_tail, p_tail = word.split('|')
            return stem + s_tail
        else:
            return word

    def plural(self, word):
        if '|' in word:
            stem, s_tail, p_tail = word.split('|')
            return stem + p_tail
        else:
            for suffix_set, chop, plural_suffix in self.patterns:
                for suffix in suffix_set:
                    if word.endswith(suffix):
                        if chop:
                            word = word[:-len(suffix)]
                        return word + plural_suffix
            # Return the base word if no matches
            return word

    def plurality(self, word, plural):
        return self.plural(word) if plural else self.singular(word)
