When working with a csv or tsv file, it is often useful to coerce the output into a given format. 
Tabby allows one to define a schema and then parse an iterable of rows into that schema.

```python
import csv
import tabby
from tabby import fields

class StopSchema(Schema):
    stop_id = fields.StringField()
    code = fields.StringField('stop_code')
    name = fields.StringField('stop_name')
    desc = fields.StringField('stop_desc')
    lat = fields.FloatField('stop_lat')
    lon = fields.FloatField('stop_lon')
    zone_id = fields.StringField()
    url = fields.StringField('stop_url')
                
with open('stops.csv', 'r') as f:
    rows = csv.reader(f)
    rows = list(StopSchema.process(rows))
      
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
