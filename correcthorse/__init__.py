# Correct Horse: A passphrase generator
#
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


from random import randint
import json
from collections import namedtuple
from locale import getlocale
import os

from .plurals import Plurality

__version__ = "0.1.1"

# The default number of words in the passphrase
DEFAULT_PP_LENGTH = 4

WordGroup = namedtuple("WordGroup", ['count', 'meta', 'words'])

class WordSet:
    def __init__(self, filename=None, locale=None, encoding="UTF-8"):
        self._group_list = []
        self._current_group = set()
        self._current_meta = {}
        self._index = {}

        if locale is None:
            locale = getlocale()[0]
        
        self._pp = Plurality(locale)

        if filename is None:
            here = os.path.split(__file__)[0]
            words_dir = os.path.join(here, "words")
            filename = os.path.join(words_dir, "words_{}.txt".format(locale))
            if not os.path.isfile(filename):
                filename = os.path.join(words_dir, "words_{}.txt".format(locale.split("_")[0]))
            if not os.path.isfile(filename):
                filename = os.path.join(words_dir, "words_en.txt")
                
        self._ingest_file(filename)

    def _add_words(self, words):
        c = self._current_group
        for w in words:
            c.add(w)

    def _push_set(self):
        l = len(self._current_group)
        if l:
            i = self.group_count
            self._current_meta['index'] = i
            if 'name' not in self._current_meta:
                self._current_meta['name'] = "Set_{}".format(i)
            self._index[self._current_meta['name']] = i
            group = WordGroup(l, self._current_meta, list(self._current_group))
            self._group_list.append(group)
            self._current_group = set()
            self._current_meta = {}

    def _ingest_file(self, filename):
        with open(filename) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    if line[0] != '#':
                        self._add_words(line.split())
                    elif line.startswith('#*'):
                        try:
                            self._current_meta.update(json.loads(line[2:]))
                        except ValueError as ex:
                            print("Error parsing metadata: {}".format(line))
                            raise ex
                else:
                    self._push_set()

    @property
    def group_count(self):
        return len(self._group_list)
                    
    def random_from_group(self, g):
        count, meta, l = g
        return l[randint(0, count-1)]

    def random_word(self):
        return self.random_word_from_groups(range(self.group_count))

    def random_word_from_lists(self, lists):
        sl = self._group_list
        tt = sum(sl[i].count for i in lists)
        index = randint(0, tt-1)
        for set_num in lists:
            count, meta, l = sl[set_num]
            if index < count:
                return (set_num, l[index])
            else:
                index -= count

    def _min_for_group(self, index):
        meta = self._group_list[index].meta
        return meta['min'] if 'min' in meta else 0

    def _max_for_group(self, index, word_count):
        meta = self._group_list[index].meta
        return meta['max'] if 'max' in meta else word_count

    def random_phrase(self, word_count=DEFAULT_PP_LENGTH):
        # Initialise table of the remaining number we are allowed to pick 
        # from any given group
        limits = dict((s.meta['name'], self._max_for_group(i, word_count))
                      for i, s in enumerate(self._group_list))

        # This sub-function is used to update limits
        def handle_meta(meta):
            limits[meta['name']] -= 1
            if 'exclude' in meta:
                for ex in meta['exclude'].split():
                    limits[ex] = 0

        # Initialise the list of words
        r = []

        # Get words for any group that has a minimum (usually just nouns)
        for group_index, group in enumerate(self._group_list):
            mm = self._min_for_group(group_index)
            if mm:
                for _ in range(mm):
                    r.append((group_index, self.random_from_group(group)))
                    handle_meta(group.meta)
                    
        # Fill up the reaining words
        while len(r) < word_count:
            # Only draw from groups that have not reached their limits
            lists = [group_index
                     for group_index, group in enumerate(self._group_list)
                     if limits[group.meta['name']] > 0]
            group_index, word = self.random_word_from_lists(lists)
            handle_meta(self._group_list[group_index].meta)
            entry = (group_index, word)
            if entry not in r:
                r.append(entry)

        # Find out if the last noun needs to be plural
        implied_count = set(group_index for group_index, word in r
                            if 'plural' in self._group_list[group_index].meta)
        if implied_count:
            plural = any(self._group_list[group_index].meta['plural']
                         for group_index in implied_count)
        else:
            plural = bool(randint(0,1))

        # Sort only on group number, not word
        r.sort(key=lambda x:x[0])
        
        # Find words that might need to be plural
        pluralise = [i for i, (group_index, word) in enumerate(r)
                     if ('pluralise' in self._group_list[group_index].meta
                         and self._group_list[group_index].meta['pluralise'])]
        
        # Set all but the last one to singular
        for i in pluralise[:-1]:
            group_index, word = r[i]
            r[i] = (group_index, self._pp.singular(word))
        if pluralise:
            i = pluralise[-1]
            group_index, word = r[i]
            r[i] = (group_index, self._pp.plurality(word, plural))
        
        return [word for group_index, word in r]

