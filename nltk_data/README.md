# spaCy

This repository contains all the files to manual recreate and install the ***en_core_web_sm model (Version 2.0.0)*** via _setup.py_ or _pip_.
Post manually recreating the folder structure, any compression software can be used to convert it to a **tar file**, which can then be installed via pip.

## File Structure

Recreate the same file structure as shown below. Unzip all the files within repository to accomplish the same.

en_core_web_sm-2.0.0 --> en_core_web_sm --> en_core_web_sm-2.0.0 --> *Place ner, parser & vocab here. "tagger" should already be present*

## Usage

Install it via pip by running ***pip install path-to-en_core_web_sm-2.0.0.tar*** within Command Prompt or by running ***python setup.py install*** within Command Prompt (Windows) after navigating to the package folder.
                                                     |
