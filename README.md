flask-mongo-session
=======================

Check it out if you need to share session and use mongodb.

## Install

```sh
pip install flask-mongo-session
```

## Usage

Set flask's `session_interface` using `MongoSessionProcessor`.

```py
from flask_mongo_session.session_processor import MongoSessionProcessor
from flask import Flask

app = Flask(__name__)
app.session_cookie_name = 'JSESSIONID'
app.session_interface = MongoSessionProcessor('mongodb://localhost:27017/your_database')
```


## Publish

```sh
python setup.py sdist upload
```


## LICENSE


The MIT License (MIT)

Copyright (c) 2018 eHanlin Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

