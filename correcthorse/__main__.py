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

from . import WordSet, DEFAULT_PP_LENGTH

import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate random memorable passphrases')
    parser.add_argument("-n", "--word-count", type=int,
                        help="set the number of words in the passphrase",
                        default=DEFAULT_PP_LENGTH)
    parser.add_argument("-l", "--lower-case",
                        action='store_true',
                        help="print all words in lower case")
    parser.add_argument("-c", "--capitalise",
                        action='store_false', dest="lower_case",
                        help="capitalise the first letter of each word")
    parser.add_argument("-u", "--underscore", dest="separator",
                        help="join the words with an underscore",
                        action='store_const', const="_")
    parser.add_argument("-s", "--space", dest="separator",
                        help="join the words with a space",
                        action='store_const', const=" ")
    parser.add_argument("-j", "--join", dest="separator",
                        help="join the words without a separator",
                        action='store_const', const="")
    parser.add_argument("-H", "--hyphen", dest="separator",
                        help="join the words with a hyphen",
                        action='store_const', const="-")
    parser.add_argument("-S", "--separator",
                        help="specify a separator to join the words")
    parser.add_argument("-f", "--word-file", metavar="FILENAME",
                        help="specify a file of words to use",
                        default=None)
    parser.add_argument("-L", "--locale", metavar="LOCALE",
                        help="specify a locale for the word set and grammar",
                        default=None)
    
    args = parser.parse_args()

    wordset = WordSet(args.word_file, locale=args.locale)
    words = wordset.random_phrase(args.word_count)

    if not args.lower_case:
        words = [w.capitalize() for w in words]

    separator = args.separator if args.separator is not None else " "
    
    print(separator.join(words))

if __name__ == "__main__":
    main()
