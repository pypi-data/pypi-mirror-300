# CuttApi

One of the best URL shortener modules for Python of all time!

CuttApi is one of the best ways of shortening URLs using Cuttly URL shortener just by entering your API key and seeing the rest that is done automatically by the Module

## Installation

Installing requirements to establish the Module:

```
requests
urllib3
pyperclip
```

**Use pip to Install the above Modules**

## Usage

The only thing users need to do is:

```python
from CuttApi import Cuttshort
import stdiomask
api_key = stdiomask.getpass("Enter your Cuttly api key: ")
short = Cuttshort(api_key)
```

* If you enter the correct API key, then you proceed.
* But if you enter a wrong one, you proceed only after entering the correct one.
* As you proceed, the same thing happens with Links and Alias (if you wanna give), but that's good since the process doesn't start over from the start of entering the API key.

## yurl

Cuttshort class is supported by one more class which is a URL corrector as well as checker!

```python
from CuttApi import yurl
a = yurl("google.com").link
print(a)
```

This returns `https://www.google.com/` And that happens whether you put:
* google.com
* http://google.com
* https://google.com
* google.com/
* http://google.com/
* https://google.com/
* www.google.com
* http://www.google.com
* https://www.google.com
* www.google.com/
* http://www.google.com/
* https://www.google.com/

## Privacy

CuttApi developer respects your privacy! The data you enter does not go over the net except to CuttLy for creations and updates. The data you enter is safely stored on your device, so that you can work on links and find them easily!

Please keep the following points in mind:
* Don't delete the file to make sure you have the best experience!
* The file is stored with the name as your API key, so any manual updates by the user to this file can cause the user not being able to use the latest feature!
* Multiple API keys can be used on the same device!

## Feedback

Feedbacks are vital for any software! You say, we make, you try @ https://cutt.ly/CuttApifeedback

## License

MIT

Copyright (c) 2024 Devraj Therani

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.