# Copyright 2011 Concentric Sky, Inc.·
#·
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#·
#   http://www.apache.org/licenses/LICENSE-2.0
#·
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__ = ['u_slugify']

# From http://stackoverflow.com/questions/702337/how-to-make-django-slugify-work-properly-with-unicode-strings
def u_slugify(txt):
    """A custom version of slugify that retains non-ascii characters. The purpose of this
    function in the application is to make URLs more readable in a browser, so there are 
    some added heuristics to retain as much of the title meaning as possible while 
    excluding characters that are troublesome to read in URLs. For example, question marks 
    will be seen in the browser URL as %3F and are thereful unreadable. Although non-ascii
    characters will also be hex-encoded in the raw URL, most browsers will display them
    as human-readable glyphs in the address bar -- those should be kept in the slug."""
    txt = txt.strip() # remove trailing whitespace
    txt = re.sub('\s*-\s*','-', txt, re.UNICODE) # remove spaces before and after dashes
    txt = re.sub('[\s/]', '_', txt, re.UNICODE) # replace remaining spaces with underscores
    txt = re.sub('(\d):(\d)', r'\1-\2', txt, re.UNICODE) # replace colons between numbers with dashes
    txt = re.sub('"', "'", txt, re.UNICODE) # replace double quotes with single quotes
    txt = re.sub(r'[?,:!@#~`+=$%^&\\*()\[\]{}<>]','',txt, re.UNICODE) # remove some characters altogether
    return txt
