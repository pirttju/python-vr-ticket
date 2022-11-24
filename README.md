# python-vr-ticket

Python kikkare for reading Aztec barcodes on VR's train tickets

## Background:

Finnish Railways (VR) uses Small Structured Barcodes (SSB) on travel documents. These are 6-layer Aztec 2D barcodes as specified in UIC leaflet 918-2. More can be read from ERA TAP TSI technical document B.6.


### Links
* https://gist.github.com/derhuerst/26c1706c1bc1d9ebae76104a14d27f97
* https://www.era.europa.eu/activities/technical-specifications-interoperability_en
* https://www.era.europa.eu/content/tap

## Dependencies:

The script depends on two packages:
* bitstring
* docbarcodes

The docbarcodes package is a wrapper for zxing which requires Java 8 environment to be installed.

## Install:

Install packages:

```
$ pip install -r requirements.txt
```

## Usage:

```
$ python python_vr_ticket.py <path_to_image>
```

python_vr_ticket reads the input image and looks for barcodes. When a barcode is succesfully found and processed, structured ticket data gets printed out.
