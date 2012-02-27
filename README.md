When working with a csv or tsv file it often useful to coerce the output into a given format. 
Tabby allows one to setup a schema and then parse an iterable of rows into that schema.

```python
import csv
import tabby
import tabby.fields

schema = [tabby.fields.StringField('stop_id'),
          tabby.fields.StringField('stop_code', key='code'),
          tabby.fields.StringField('stop_name', key='name'),
          tabby.fields.StringField('stop_desc', key='desc'),
          tabby.fields.FloatField('stop_lat', key='lat'),
          tabby.fields.FloatField('stop_lon', key='lon'),
          tabby.fields.StringField('zone_id'),
          tabby.fields.StringField('stop_url', key='url'),
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