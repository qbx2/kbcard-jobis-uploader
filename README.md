# Kbcard Jobis Uploader

This script reads breakdown excel files in kbcard format.
Then the script generates receipt images from the rows and
asks which images should be uploaded. The selected images will be on your jobis.

## Installation

```
$ pip install -r requirements.txt
```

It should install pillow and xlrd.

## Usage

1. Run generate.py [breakdown xls file]
1. Run upload.py [generated directory]

## URLs

* Kbcard breakdown - https://card.kbcard.com/CXPRIMYS0007.cms
* Jobis - https://jobis.co/
