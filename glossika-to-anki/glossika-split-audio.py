#!/usr/bin/env python3

import glob
import os
import re
import subprocess
import sys


src_dir = 'glossika_src_data/audio'
out_dir = 'glossika_output/audio'

if not os.path.exists(src_dir):
    os.makedirs(src_dir)
    sys.exit('\nCreated {}\n'
             'Copy GMS-C mp3 files into this folder and re-run.\n'
             'Files can be within sub-folders.'.format(src_dir))

files = glob.glob(os.path.join(src_dir, '**/EN*-GMS-C-????.mp3'),
                  recursive=True)
print('\nProcessing {} files...\n'.format(len(files)))

for f in sorted(files, key=lambda x: re.search('(\d{4})', x).group(1)):
    f_name = f.split('/')[-1]
    print('Processing {}'.format(f_name))

    re_match = re.search('EN(.{2,4})-..-GMS-C-(\d{4}).mp3', f)
    if not re_match:
        print('File name does not match\n'
              'Skipping {}'.format(f_name))
        continue
    language = re_match.group(1)
    from_phrase = int(re_match.group(2))
    to_phrase = from_phrase + 49

    """
    Run mp3splt
    Parameters tested with:
        mp3splt 2.6.2 (09/11/14) - using libmp3splt 0.9.2
    -n No tags. Allows you to concatenate the files later
    -x No Xing headers. Same as above
    -s Silence mode ~ split files with silence detection
    -p Parameters for silence mode
        rm=0.2_0 Remove silence between tracks. Leaves 0.2 at beginning
            and 0 at the end
        min=1.9 Split on a minimum of 1.9 seconds of silence
        shots=12 Min shots following silence to qualify. Decreased from
            default of 24 for small sentences
    -o @N3 Name output files with 3 digit ints
    -d Output directory
    """
    st = subprocess.run(
        args=['mp3splt', '-n', '-x', '-s', '-p',
              'rm=0.2_0,min=1.9,th=-64,shots=12',
              '-o', '@N3', '-d', out_dir, f],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if st.returncode != 0:
        sys.exit('Something went wrong...\nCheck files and retry.')

    s_files = glob.glob(os.path.join(out_dir, '???.mp3'))
    if len(s_files) != 54:
        sys.exit('Expected 54 files but got {}.\n'
                 'Aborting at {}'.format(len(s_files), f_name))

    # Rename files sequentially and skip Glossika intro & outro
    s_files = sorted(s_files)[2:52]
    count = from_phrase
    for f in s_files:
        name = '{}-{:04d}.mp3'.format(language, count)
        count += 1
        os.rename(f, os.path.join(out_dir, name))
for f in glob.glob(os.path.join(out_dir, '???.mp3')):
    os.remove(f)
os.remove('mp3splt.log')
print('\nComplete!')
