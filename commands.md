### Using fixtures to provide initial data for models

- to create a fixtures:
`python manage.py dumpdata courses --indent=2`
- Save data in fixtures/ directory:
```python manage.py dumpdata courses --indent=2 --output=courses/fixtures/subjects.json```
- load the fixture into the database:
`python manage.py loaddata subjects.json`