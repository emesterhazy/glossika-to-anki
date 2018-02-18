#!/usr/bin/env python3

import csv
from collections import defaultdict
import genanki
import glob
import os
import re
import sys
import yaml


# TODO: Currently only includes Mandarin template
def main():
    print('\nStarting Anki generation...')
    call_dir = os.getcwd()
    out_dir = 'glossika_output'
    audio_dir = os.path.join(out_dir, 'audio')

    # Dict to hold language options
    langs = {}
    langs['ZS'] = {
        'fields': get_template('zs-fields.yml'),
        'template': get_template('zs-template.yml'),
        'css': get_template('zs-css.css')}

    # Define genanki models here. See the genanki documentation for details
    langs['ZS']['model'] = genanki.Model(
        model_id = 1546318185,  # Must be unique and random; see genanki docs
        name = 'Glossika ZS',
        fields = langs['ZS']['fields'],
        templates= [langs['ZS']['template']],
        css = langs['ZS']['css'])

    # Define genanki decks here
    langs['ZS']['deck'] = genanki.Deck(
        deck_id = 1507569441,  # Must be unique and random; see genanki docs
        name = 'Glossika Mandarin (Mainland)')

    if not os.path.exists(audio_dir):
        sys.exit('Audio output folder missing.\n'
                 'Run audio split script again and retry.')

    # Generate Anki Decks
    tsv_files = glob.glob(os.path.join(out_dir, 'GLOSSIKA-EN*-EBK.tsv'))
    languages = defaultdict(list)
    for tsv in sorted(tsv_files):
        re_match = re.search('(GLOSSIKA-EN(.{2,4})-..-EBK)\.tsv', tsv)
        if re_match:
            languages[re_match.group(2)].append(tsv)

    for lang in languages:
        # Load sentences
        sentences = []
        for tsv in sorted(languages.get(lang)):
            with open(tsv, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect='excel-tab')
                sentences.extend(list(reader))

        mp3_paths = glob.glob(
            os.path.join(audio_dir, '{}-????.mp3'.format(lang)))
        mp3_names = sorted([mp3.split(os.sep)[-1] for mp3 in mp3_paths])
        if len(sentences) != len(mp3_names):
            print('Sentences ({:,d}) mismatched with mp3s ({:,d})\n'
                  'Skipping this language. '
                  'Re-extract Glossika source and try again.'
                  .format(len(sentences), len(mp3_names)))
            continue

        # Create deck
        glossika_deck = langs[lang]['deck']
        for sent, audio in zip(sentences, mp3_names):
            note = genanki.Note(
                model=langs[lang]['model'],
                # TODO: adjust number of fields by language
                fields=[
                    '[sound:{}]'.format(audio), sent[1], sent[2], sent[0], ''])
            glossika_deck.add_note(note)

        # Generate the Anki deck
        os.chdir(audio_dir)  # Required for Anki generation, see genanki docs
        pkg = genanki.Package(glossika_deck)
        pkg.media_files = mp3_names
        deck_name = '{}.apkg'.format(glossika_deck.name)
        pkg.write_to_file(deck_name)
        os.chdir(call_dir)

        # Clean up
        for x in [languages.get(lang), mp3_paths]:
            for y in x:
                os.remove(y)
        os.rename(os.path.join(audio_dir, deck_name),
                  os.path.join(out_dir, deck_name))
        try:
            os.rmdir(audio_dir)
        except OSError:
            pass

        print('Finished {}'.format(deck_name))


def get_template(f_name):
    project_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(os.path.join(project_dir, 'templates', f_name),
                  'r', encoding='utf-8') as f:
                if f_name[-3:] == 'yml':
                    return yaml.load(f)
                elif f_name[-3:] == 'css':
                    return f.read()
                else:
                    return None
    except FileNotFoundError:
        sys.exit('Missing template file {}. Try again.'.format(f_name))


if __name__ == '__main__':
    main()
