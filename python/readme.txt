To run:

> python eyedetect.py .\testimages\face1.jpg

If debug is enabled, the script will display the input filename:

Input file: .\testimages\face1.jpg

It will then display the input image, and search for faces, telling the user the number of faces found:

1 faces found.

and save the face to \extractedfeatures\faces\face1.png
Then search for eyes, and tell the user how many of those were found:

2 eyes found.

and save the eyes to \extractedfeatures\eyes\face1-1.png,face1-2.png.
And lastly display the input image with the face boxed in blue and the eyes boxed in green.