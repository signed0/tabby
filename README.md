When working with a csv or tsv file it often useful to coerce the output into a given format. 
Tabby allows one to setup a schema and then parse a iterable of rows into that schema.

```python
import csv
import tabby

schema = [fields.StringField('stop_id'),
          fields.StringField('stop_code', key='code'),
          fields.StringField('stop_name', key='name'),
          fields.StringField('stop_desc', key='desc'),
          fields.FloatField('stop_lat', key='lat'),
          fields.FloatField('stop_lon', key='lon'),
          fields.StringField('zone_id'),
          fields.StringField('stop_url', key='url'),
          ]
                
with open('file.csv', 'r') as f:
    rows = csv.reader(f)
    rows = list(tabby.parse(rows, schema))
      
>>> print rows[0]
{'code': '12925', 
 'name': 'MATILDA @ LEWIS - S - NS',
 'url': None,
 'lon': -96.7686,
 'zone_id': None,
 'stop_id': '12925', 
 'lat': 32.812256, 
 'desc': None
 }
```                