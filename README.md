# glossika-to-anki
*Generate Anki decks from Glossika PDFs and audio files*

`glossika-to-anki` is a set of Python 3 scripts to generate Anki flashcards using the PDFs and audio from the [Glossika](https://ai.glossika.com/?lang=eng-US) language program.

## Features
`glossika-to-anki` provides three main utilities:

1. `glossika-extract-pdf.py` - Generate a TSV file of English and target language phrases from Glossika PDFs
2. `glossika-split-audio.py` - Split GMS-C audio files into individual mp3s for each phrase
3. `generate_anki.py` - Create an Anki deck by combining each phase and its corresponding audio into a separate Anki note / card

## Requirements & Setup
1. [Python 3](https://www.python.org/)
    - On Windows you can run the installer from the Python website.
    - MacOS or Linux you can install python with `brew install python` or `apt install python`.
2. [pdftotext](https://www.xpdfreader.com/download.html) - Converts the Glossika PDFs to text so that the phrases can be extracted with regex.
    - On Windows download [Xpdf tools](https://www.xpdfreader.com/download.html) and copy pdftotext.exe to a folder on the path (i.e. the Python folder). If you installed python with the Windows installer, the default path should be ```C:\Program Files``` or ```C:\Users\your_name\AppData\Local```. Alternatively, you might also be able to run  ```which python``` or ```where python``` from cmd prompt to figure out where the python executable is located.

    - On MacOS `brew cask install pdftotext`; on Linux `apt install poppler-utils`
3. [mp3splt](http://mp3splt.sourceforge.net/) - Splits the GMS-C files into individual files on the silence between sentences.
    - On Windows download mp3splt from the project homepage and add it to the path
    - On MacOS `brew install mp3splt`; on Linux `apt install mp3splt`
4. [genanki](https://github.com/kerrickstaley/genanki) to generate Anki decks
    - `pip install genanki` or `pip3 install genanki`
5. *v2 Glossika PDFs and GMS-C mp3 files*
    - The PDF script only works with the v2 Glossika PDFs. These files are searchable, and have a blue box around each phrase. If your PDFs are more than 20 mb you have the older version that is not supported.
    - Here's an example of what the audio file names should look like: `ENZS-F1-GMS-C-0001.mp3`. Note that the ENZS prefix
        is for Mandarin and varies by language.
    - *Note:* The Glossika PDFs and audio files are difficult to find since Glossika recently discontinued them and launched a subscription service. I heard some people have had luck contacting Glossika's support team to purchase the older PDF courses, but your milage may vary.

## Running
Clone or download the repository.
```
git clone git@github.com:emesterhazy/glossika-to-anki.git
cd glossika-to-anki/glossika-to-anki
```
Run each script and follow the prompts to copy the Glossika files into the source folder that is created.
```
python glossika-extract-pdf.py
python glossika-split-audio.py
python generate_anki.py
```
Import your new Anki deck!

## Limitations
1. Only supports the v2 Glossika PDFs, not the older non-searchable PDFs. PDFs with copy protection must have it removed before sentences can be extracted.

2. No support for extracting IPA

## Contributing
Pull requests are welcome. If you would like to add support for the v1 Glossika PDFs or make changes that require new dependencies please open an issue first to discuss.
