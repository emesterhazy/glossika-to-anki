#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import glob
import os
import re
import subprocess
import sys


def main():
    # Dictionary of languages and sentence markers.
    # If your language isn't listed, add it here

    languages = {
        'ZS': ['EN', '简', 'PIN'],  # Simplified Chinese
        'ZH': ['EN', '繁', 'PIN'],  # Traditional Chinese
        'ZT': ['EN', '繁', 'PIN'],  # Traditional Chinese (Taiwan)
        'YUE': ['EN', '粵', 'YALE'],  # Cantonese | Change YALE to JYUT for Jyutping
        'JA': ['EN', '日', 'ROM']   # Japanese
    }

    src_dir = os.path.join('glossika_source', 'pdf')
    out_dir = 'glossika_output'

    if not os.path.exists(src_dir):
        os.makedirs(src_dir)
        sys.exit('\nCreated {}\n'
                 'Copy pdf files into this folder and re-run'.format(src_dir))

    files = glob.glob(os.path.join(src_dir, 'GLOSSIKA-EN*-EBK.pdf'))
    if len(files) == 0:
        print('\nNo matching PDF files detected.\n'
              'Refer to the readme for the required file name pattern.')
        return
    else:
        pass
    print('\nProcessing {} files...\n'.format(len(files)))

    for f in sorted(files):
        f_name = f.split(os.sep)[-1]
        print('Processing  {}...'.format(f_name), end='')

        re_match = re.search('(GLOSSIKA-EN(.{2,4})-..-EBK)\.pdf', f)
        if not re_match:
            print('unmatched')
            print('File name does not match\n'
                  'Skipping {}'.format(f_name))
            continue

        csv_file = '{}/{}.tsv'.format(out_dir, re_match.group(1))
        text_pdf = '{}/{}.txt'.format(out_dir, re_match.group(1))
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        # Set language flags to search for
        if re_match.group(2) in languages:
            lang_flags = languages.get(re_match.group(2))
        else:
            lang_flags = ['EN', re_match.group(2)]

        # Try to delete text version of pdf if it exists
        if os.path.exists(text_pdf):
            try:
                os.remove(text_pdf)
                convert_pdf(f, text_pdf)
            except OSError as e:
                print('file locked... using existing text version of pdf')
        else:
            convert_pdf(f, text_pdf)

        pdf = open(text_pdf, encoding='utf-8')
        lang_ix = 0  # Track which type of phrase is next
        indent_level = 0  # Track indentation for muiti-line sentences
        current_phrase = []  # Set of phrases
        phrases = []
        for line in pdf:
            line = line.rstrip('\n')

            if indent_level > 0:
                # Match continuing sentence based on indentation level
                r = re.match('(\s{{{}}})(\S.*)'.format(indent_level), line)
                if r:
                    current_sent += ' ' + r.group(2)
                    continue
                else:
                    indent_level = 0
                    lang_ix += 1
                    current_phrase.append(current_sent)
                    if lang_ix >= len(lang_flags):
                        lang_ix = 0
                        phrases.append(current_phrase)
                        current_phrase = []

            # Match sentence by finding language flag
            r = re.match('(\s+{}\s+)(\S.*)'.format(lang_flags[lang_ix]), line)
            if not r:
                continue
            current_sent = r.group(2)
            indent_level = len(r.group(1))

        if len(phrases) != 1000:
            print('error')
            print('Something went wrong...'
                  'found {} sentences instead of 1,000'.format(len(phrases)))
            continue

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='excel-tab')
            for phrase in phrases:
                writer.writerow(phrase)
        pdf.close()
        os.remove(text_pdf)
        print('complete')

    print('PDF extract complete!')


def convert_pdf(f, text_pdf):
    st = subprocess.run(
        args=['pdftotext', '-layout', '-enc', 'UTF-8', f, text_pdf],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if st.returncode != 0:
        print('error')
        sys.exit('PDF conversion failed. '
                 'Remove copy protection and retry.\n')


if __name__ == '__main__':
    main()
