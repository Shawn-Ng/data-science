# BeautifulSoup Cheatsheet
1. [Basic](#1-basic)
2. [Make soup](#2-make-soup)
3. [Output](#3-output)
4. [Search](#4-search)
5. [Navigation](#5-navigation)
6. [Edit](#6-edit)
7. [Encoding](#7-encoding)
8. [Parse only part](#8-parse-only-part)





## 1. Basic
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'lxml')


soup.title
# >>> <title>The Dormouse's story</title>
soup.title.name
# >>> u'title'
soup.title.string
# >>> u'The Dormouse's story'
soup.title.parent.name
# >>> u'head'

# css finder
css_soup.select("p.strikeout.body")

soup.p
# >>> <p class="title"><b>The Dormouse's story</b></p>
soup.p['class']
# >>> u'title'
soup.a
# >>> <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
soup.find_all('a')
# >>> [<a ..>, ..]
soup.find(id="link3")
# >>> <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

for link in soup.find_all('a'):
    print(link.get('href'))
# >>> http://example.com/elsi, # http://example.com/lacie
```





## 2. Make soup
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("index.html"))
soup = BeautifulSoup("<html>data</html>")
```





## 3. Output
```python
# HTML
# pretty print
soup.prettify()
# non-pretty print
str(soup)

# STRING
# all text under the element
soup.get_text()
```




## 4. Search
```python
#-------------------------
# CSS SELECTOR
#-------------------------
css_soup.select("p.strikeout.body")
soup.select("head > title")

# direct child
soup.select("p > #link1")
# 3rd child
soup.select("p nth-of-type(3)")
soup.select("p > a:nth-of-type(2)")

# sibling
soup.select("#link1 ~ .sister")  
# existence of an attribute
soup.select('a[href]')
soup.select_one(".sister")

# ATTRIBUTE VALUE
# exact attribute
soup.select('a[href="http://example.com/elsie"]')
# negative match
soup.select('a[href^="http://example.com/"]')
# end match
soup.select('a[href$="tillie"]')
# middle match
soup.select('a[href*=".com/el"]')


#-------------------------
# BASIC
#-------------------------
# match by tag
soup.find_all('b')
# match by tag using regex
soup.find_all(re.compile("^b"))
# match by tag in list
soup.find_all(["a", "b"])

# function (complex condition)
def has_class_but_no_id(tag):
  return tag.has_attr('class') and not tag.has_attr('id')

soup.find_all(has_class_but_no_id)


#-------------------------
# find_all
#-------------------------
find_all(name, attrs, recursive, string, limit, **kwargs)

# tag condition
soup.find_all("title")
# tag and attr
soup.find_all("p", "title")
# >>> [<p class="title"><b>The Dormouse's story</b></p>]
soup.find_all("a")

# keyword arguments
soup.find_all(id="link2")
soup.find_all(href=re.compile("elsie"), id='link1')
soup.find(string=re.compile("sisters")) # text contain sisters

# css class (class is researved keyword)
soup.find_all("a", class_="sister")
```




## 5. Navigation
```python
#-----------------------------
# going up/down/side
#-----------------------------
# ----- going down -----
soup.head
# >>> <head><title>The Dormouse's story</title></head>
soup.title
# >>> <title>The Dormouse's story</title>
soup.body.b
# >>> <b>The Dormouse's story</b>
soup.a
# >>> <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http:

# children = contents
head_tag.contents
# >>> [<title>The Dormouse's story</title>]
head_tag.children
# >>> [<title>The Dormouse's story</title>]

# descendants (all of a tag’s children, recursively)
for child in head_tag.descendants:
  print(child)

# .string is tricky
head_tag.contents
# >>> [<title>The Dormouse's story</title>]
head_tag.string
# >>> u'The Dormouse's story' (because head tag has only one child)
print(soup.html.string)
# >>> None (because html has many children)

# whitespace removed strings
for string in soup.stripped_strings:
  print(repr(string))


# ----- GOING UP -----
title_tag.parent # <head><title>The Dormouse's story</title></head>
# going up recursively
link.parents # [ p, body, html, [document], None]


# ----- SIDEWAY -----
# sibling = include text node
sibling_soup.b.next_sibling
sibling_soup.c.previous_sibling

# multiple
sibling_soup.b.next_siblings
sibling_soup.c.previous_siblings

# element = not include text node
sibling_soup.b.next_element
sibling_soup.c.previous_element
sibling_soup.b.next_elements
sibling_soup.c.previous_elements
```




## 6. Edit
``` python
#----------------------------
# CHANGE EXISITNG TAG
#----------------------------
# modify tag name
tag.name = "blockquote"
# modify tag attribute
tag['class'] = 'verybold'
# delete attribute
del tag['class']
# modify tag contents string
tag.string= 'not too bold'
# append tag contents
tag.append(" but bolder than usual")

#----------------------------
# INSERT TAG
#----------------------------
new_tag = soup.new_tag("a", href="http://www.example.com")
# create child
original_tag.append(new_tag)
# can edit element after creating child
new_tag.string = "Link text."

soup.b.string.insert_before(tag)
soup.b.i.insert_after(soup.new_string(" ever "))

#----------------------------
# DELETE TAG
#----------------------------
# removes the contents
soup.i.clear()
# completely removes a tag from tree and returns the element
i_tag = soup.i.extract()
# completely removes a tag from tree and discard the tag
soup.i.decompose()

#----------------------------
# REPLACE/WRAP/UNWRAP TAG
#----------------------------
a_tag.i.replace_with(soup.new_tag("b"))
# replace inner html
a_tag.i.replace_with(Beautifulsoup("<b>bold element</b>"))
soup.p.string.wrap(soup.new_tag("b"))
a_tag.i.unwrap()
```




## 7. Encoding
```python
# output
soup.prettify("latin-1")
tag.encode("utf-8")
tag.encode("latin-1")
tag.encode("ascii")
```




## 8. Parse only part
```python
# The SoupStrainer class allows you to choose which parts of an
# incoming document are parsed
from bs4 import SoupStrainer

# conditions
only_a_tags = SoupStrainer("a")
only_tags_with_id_link2 = SoupStrainer(id="link2")

def is_short_string(string):
  return len(string) < 10
only_short_strings = SoupStrainer(string=is_short_string)

# execute parse
BeautifulSoup(html_doc, "html.parser", parse_only=only_a_tags)
BeautifulSoup(html_doc, "html.parser", parse_only=only_tags_with_id_link2)
BeautifulSoup(html_doc, "html.parser", parse_only=only_short_strings)
```
