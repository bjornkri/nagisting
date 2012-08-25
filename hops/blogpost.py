import codecs
import datetime
from os import popen
from BeautifulSoup import BeautifulSoup


class BlogPost(object):

    def __init__(self, infile):
        super(BlogPost, self).__init__()
        self.meta = {}
        self.text = u""
        self.html = u""
        self.parse_file(infile)

    def parse_file(self, infile):
        file_obj = codecs.open(infile, mode="r", encoding="utf8")
        current_line = file_obj.readline().strip()
        while len(current_line):
            if current_line[0] == u'\ufeff':
                current_line = current_line[1:]
            self.add_meta(current_line.encode('ascii', 'xmlcharrefreplace'))
            current_line = file_obj.readline().strip()

        filename = file_obj.name.split('/')[-1]
        self.meta['slug'] = filename.split('_')[1][:-4]

        self.meta['pubdate'] = datetime.datetime.strptime(
            self.meta['pubdate'], '%a %b %d %H:%M:%S %Y')

        html = popen('multimarkdown %s' % infile).read()
        soup = BeautifulSoup(html)
        self.html = "".join(unicode(x) for x in soup.body)

    def get_header(self):
        if 'title' in self.meta:
            if 'link' in self.meta:
                ret_val = u"<h1><a href='%s' class='ext'>%s</a> <a href='%s' class='bs'>&rarr;</a></h1>\n\n" % (
                    self.meta['link'],
                    self.meta['title'].encode('ascii', 'xmlcharrefreplace'),
                    self.get_absolute_url()
                )
            else:
                ret_val = u"<h1><a href='%s' class='bs'>%s</a></h1>\n\n" % (
                    self.get_absolute_url(), self.meta['title']
                )
        ret_val += u"<div class='date'>%s</div>" % (self.meta['pubdate'].strftime("%b %d %Y"),)
        return ret_val

    def get_absolute_url(self):
        year = self.meta['pubdate'].year
        month = self.meta['pubdate'].month
        day = self.meta['pubdate'].day
        return "/%s/%02d/%02d/%s/" % (year, month, day, self.meta['slug'])

    def add_meta(self, text):
        name, data = text.split(':')[0], (':'.join(text.split(':')[1:]).strip())
        self.meta[name.lower()] = data
