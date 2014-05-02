CoCParser
---------

Clash of Clans(이하 CoC)의 클랜전 결과 스크린샷 분석기.

각 전투의 결과(공격자, 별 갯수)를 분석하기 위한 도구

## Modules

* `flickr.py`: download images from flickr
* `labeler.py`: helper module for labeling existing images.
* `parse.py`: helper module parses images to fetch slits.
* `write_src.py`: reads all images and write them into databases
* `read_sql.py`: reads images from database and label some of them.
* `viewer/`: view result in web browser
