When working with a csv or tsv file it often useful to coerce the output into a given format. 
Tabby allows one to setup a schema and then parse a iterable of rows into that schema.

```python
import csv
import tabby

route_schema = [fields.StringField('agency_id'),
                fields.StringField('route_id'),           
                fields.StringField('route_long_name', key='long_name'),
                fields.StringField('route_short_name', key='short_name'),
                fields.ColorField('route_color', key='color', default='FFFFFF'),
                fields.ColorField('route_text_color', key='text_color', default='000000'),
                fields.StringField('route_desc', key='desc'),
                fields.StringField('route_type', key='type'),
                fields.StringField('route_url', key='url')
                ]
                
with open('routes.txt', 'r') as f:
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