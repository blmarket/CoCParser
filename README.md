CoCParser
---------

Clash of Clans screenshot parser using machine learning.
You can easily get valuable features from each clan wars.

Try http://coc.blmarket.net/ for running example.

Currently project is not yet for public use(you need to learn how to upload image, etc.), so feel free to contact me via email or file an issue on GitHub if you like to use and improve this project.

## Modules

* `flickr.py`: download images from flickr
* `labeler.py`: helper module for labeling existing images.
* `parse.py`: helper module parses images to fetch slits.
* `write_src.py`: reads all images and write them into databases
* `read_sql.py`: reads images from database and label some of them.
* `viewer/`: view result in web browser
* `feature.py`: feature extract from images and try to evaluate who's doing most effective attacks
