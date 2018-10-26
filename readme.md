# offset-mimic

Simple little script to mimic the offsets to another consumer group for a given topic. Destination consumer group does not have to exist for this to work, one will be made/committed.

## Usage

```
usage: mimic.py [-h] [--for-real] [-b BROKERS] TOPIC FROM_GROUP TO_GROUP

Mimic offsets for consumer group under topic to another consumer group.

positional arguments:
  TOPIC                 topic to inspect
  FROM_GROUP            consumer group to get offsets from
  TO_GROUP              consumer group to copy offsets to

optional arguments:
  -h, --help            show this help message and exit
  --for-real            really mimic the offsets
  -b BROKERS, --brokers BROKERS
                        kafka brokers
```

## Examples

Dry run to show you the offsets from originating group:

```
$ python mimic.py app app-prod test-atl01-es-1 -b kafka01.logs.prod.atl01:9092
Topic status for "app:app-prod", with 32 partitions:

       #  Current offset
       0: 3945242083
       1: 3945250408
       2: 3945267188
       3: 3945285344
       4: 3945293756
       5: 3944540152
       6: 3945273039
       7: 3944570301
       8: 3945261785
       9: 3945257950
      10: 3945213287
      11: 3944577309
      12: 3944610956
      13: 3945277297
      14: 3945260132
      15: 3945287472
      16: 1832762094
      17: 1832712154
      18: 1832792080
      19: 1832738112
      20: 1832154924
      21: 1832752008
      22: 1832758078
      23: 1832746335
      24: 1832737481
      25: 1832744410
      26: 1832177070
      27: 1832780783
      28: 1832778087
      29: 1832046408
      30: 1832772851
      31: 1832730787

Dry run mode, exiting
```

Real run copying offsets to another group:

```
$ python mimic.py app app-prod test-atl01-es-1 -b kafka01.logs.prod.atl01:9092 --for-real
Topic status for "app:app-prod", with 32 partitions:

       #  Current offset
       0: 3945244078
       1: 3945252319
       2: 3945269222
       3: 3945287373
       4: 3945295797
       5: 3944542162
       6: 3945274944
       7: 3944572293
       8: 3945263706
       9: 3945259931
      10: 3945215260
      11: 3944579306
      12: 3944613082
      13: 3945279580
      14: 3945262247
      15: 3945289584
      16: 1832764151
      17: 1832714287
      18: 1832794239
      19: 1832740206
      20: 1832156880
      21: 1832753970
      22: 1832760069
      23: 1832748290
      24: 1832739558
      25: 1832746499
      26: 1832179122
      27: 1832782793
      28: 1832780071
      29: 1832048301
      30: 1832774839
      31: 1832732780


After offset mimic:

Topic status for "app:test-atl01-es-1", with 32 partitions:

       #  Current offset
       0: 3945244078
       1: 3945252319
       2: 3945269222
       3: 3945287373
       4: 3945295797
       5: 3944542162
       6: 3945274944
       7: 3944572293
       8: 3945263706
       9: 3945259931
      10: 3945215260
      11: 3944579306
      12: 3944613082
      13: 3945279580
      14: 3945262247
      15: 3945289584
      16: 1832764151
      17: 1832714287
      18: 1832794239
      19: 1832740206
      20: 1832156880
      21: 1832753970
      22: 1832760069
      23: 1832748290
      24: 1832739558
      25: 1832746499
      26: 1832179122
      27: 1832782793
      28: 1832780071
      29: 1832048301
      30: 1832774839
      31: 1832732780
```
