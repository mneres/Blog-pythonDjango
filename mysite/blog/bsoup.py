from bs4 import BeautifulSoup, Comment
import re

def safe_html(html):

    if not html:
        return None

    # remove these tags, complete with contents.
    blacklist = ["script", "style","link", "meta", "head", "form", "img"]

    whitelist = [
        "div", "span", "p", "br",
        "table", "tbody", "thead", "tr", "td", "a",
        "blockquote", "b", "em", "i", "strong", "u", "font", "title",
        "h1", "h2", "h3", "h4", "h5", "h1"
    ]

    soup = BeautifulSoup(html, "html.parser")

    '''if soup.findAll("article"):
        param = "article"

    # now strip HTML we don't like.
    if param != "":
        for tag in soup.findAll(param):
            if tag.name != param:
                tag.extract()
            else:
                tag.attrs = [(a[0], safe_css(a[0], a[1])) for a in tag.attrs if _attr_name_whitelisted(a[0])]
    else:'''
    for tag in soup.findAll():
        if (len(tag.text) == 0) or (tag.name.lower() in blacklist) or (tag.name.lower() == "ul"):
            tag.extract()
        else:
            tag.attrs = [(a[0], safe_css(a[0], a[1])) for a in tag.attrs if _attr_name_whitelisted(a[0])]

    # scripts can be executed from comments in some cases
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    safe_html = str(soup)

    if safe_html == ", -":
        return None

    return safe_html


def clear_menu(soup):

    for tag in soup.findAll():
        print(tag.string)

    return soup

def _attr_name_whitelisted(attr_name):
    return attr_name.lower() in ["href", "style", "color", "size", "bgcolor", "border"]

def safe_css(attr, css):
    if attr == "style":
        return re.sub("(width|height):[^;]+;", "", css)
    return css