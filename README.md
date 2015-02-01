CoCParser
---------

Clash of Clans(이하 CoC)의 클랜전 결과 스크린샷 분석기.

각 전투의 결과(공격자, 별 갯수)를 분석하기 위한 도구

## Updates

### `feature.py` implementation

우리편의 이름은 random forest로 학습했지만, 상대방의 이름은 그렇게 할 수 없기 때문에, 대책으로 image에서 feature point를 뽑아내어 같은 이름을 분류하는 기능을 적용함.

특정 상대에 대한 공격 중에 가장 많은 별을 뽑아낸 공격자를 찾아 라벨링을 하도록 함.

#### Usage

```
python feature.py 20150130
```

## Modules

* `flickr.py`: download images from flickr
* `labeler.py`: helper module for labeling existing images.
* `parse.py`: helper module parses images to fetch slits.
* `write_src.py`: reads all images and write them into databases
* `read_sql.py`: reads images from database and label some of them.
* `viewer/`: view result in web browser
* `feature.py`: feature extract from images and try to evaluate who's doing most effective attacks
