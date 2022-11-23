# python-vr-ticket

Python kikkare for reading Aztec barcodes on VR's train tickets

## Dependencies:

docbarcodes package is a wrapper for zxing which requires Java 8.

## Install:

Install packages:

```
$ pip install -r requirements.txt
```

## Usage:

```
$ python python_vr_ticket <path_to_image>
```

python_vr_ticket reads the input image and looks for barcodes. When a barcode is found, structured ticket data is printed out.
