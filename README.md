# pic_2_pdf_for_music_sheet
Convert pictures of music sheet to a pdf file with table of contents, with support of Chinese characters.

## Requirement
```
pip install reportlab
pip install pypdf2
```

## How to use
1. Put music sheet folders to /music, with the name of the folders the same as the music. And the pics in the folder named as 1,2,3, ... in the correct order. 
2. run 
```
python pic2pdf.py
```