# svba

svba is a web-based interface to keep track of StockStram. You can find the main
svba instance [here](https://svba.null.ist). It runs in flask and your wsgi
implementation of choice.

To keep the data updated, you'll have to set up cron jobs that run `gen_data.py`
every five minutes and `gen_digest.py` every 30 minutes. These intervals can,
of course, be changed.

Enabling gzip compression (and caching of compressed files) in your server is
highly recommended—data file sizes reduced by up to 90% are noticable at
compression level 9.


>The following licenses apply to svba:
>
>All code within this repository:
>
>>Copyright 2017 Johannes Neubrand
>>
>>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>>
>>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>>
>>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
>
>digest-static.json: [CC0](https://creativecommons.org/choose/zero/).
>
>images: All rights reserved.
