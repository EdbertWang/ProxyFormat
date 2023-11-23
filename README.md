# PROXY FORMATTER
The goal of this repository is to create an easy way to turn decklists into printable proxies. This as

## Key Assumptions
The program currently assumes that you will be using standard letter sized paper (8.5 inch * 11 inch), and standard Magic the Gathering card sizes (2.5 inch * 3.5 inch). Other sizes are currently not supported.

## Running
1. Ensure that dependencies are installed.

        pip install -r requirements.txt

2. The following command will launch the input phase of the program, which will parse cards in the formats noted in the format section. I recomend copy pasting cards from an online deck building website like Moxfield. Once finished entering cards, type "end" to finish inputting cards.

        python3 format.py

    This will also work if your version of python is lower than 3.

        python format.py

3. Images will be saved into the images folder, output.pdf is the resultant pdf, and ErrorLog.txt will describe anything that went wrong.

4. The pdf should now be directly printable. This has yet to be tested.

### Formatting
The parser should accept input from any of the following sources:

* TCGPLAYER - Verified Functional
* CARD KINGDOM - Verified Functional
* MOXFIELD - Verified Functional
* ARCHIDECKT - Verified Functional

### Notes
Some dual faced cards can cause some issues. Its currently unknown if that is an issue with the code, or with Scryfall API. These cards will simply be skipped and noted in the error log.

I have removed the functionality to grab arena only versions because it makes it marginally easier to implement.