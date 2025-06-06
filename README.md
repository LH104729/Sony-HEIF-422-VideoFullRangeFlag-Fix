This Python script fixes an issue where 10-bit HEIF 4:2:2 images are displayed incorrectly due to the VideoFullRangeFlag being set to 'limited' instead of 'full'.

- This was fixed by Sony for the a7C II in firmware version 2.0.0.
- As of firmware version 1.0.3, this issue has not been fixed for the a6700.

> [!WARNING] 
> Backup your files before running this script.

Usage:

`python3 fix.py --input <input file/dir>`

Reference: 

https://www.reddit.com/r/SonyAlpha/comments/1kcprt9/a7cii_firmware_20_fixed_10bit_heif_viewing_on/

https://exiftool.org/TagNames/QuickTime.html#ColorRep