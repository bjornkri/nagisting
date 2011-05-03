import codecs
import datetime
import markdown

class BlogPost(object):

    def __init__(self, infile):
        super(BlogPost, self).__init__()
        self.meta = {}
        self.text = ""
        self.html = ""
        self.parse_file(infile)
        
    
    def parse_file(self, infile):
        file_obj = codecs.open(infile, mode="r", encoding="utf8")
        current_line = file_obj.readline().strip()
        # Strip possible \ufeff from the first line
        if current_line[-8:] == "--------": 
            current_line = file_obj.readline().strip()
            while not current_line == "--------":
                self.add_meta(current_line)
                current_line = file_obj.readline().strip()
        else:
            self.text = current_line
            print "No metadata in %s" % file_obj.name
        
        filename = file_obj.name.split('/')[-1]
        self.meta['slug'] = filename.split('_')[1][:-4]
        
        self.meta['pubdate'] = datetime.datetime.strptime(
            self.meta['pubdate'], '%a %b %d %H:%M:%S %Y')
        
        for current_line in file_obj:
            self.text += current_line
        file_obj.close()
        
        self.html = markdown.markdown(self.text)
        
    
    def get_header(self):
        if 'title' in self.meta:
            if 'link' in self.meta:
                ret_val = "<h1><a href='%s' class='ext'>%s</a> <a href='%s' class='bs'>&beta;</a></h1>\n\n" % (
                    self.meta['link'],
                    self.meta['title'],
                    self.get_absolute_url()
                )
            else:
                ret_val = "<h1><a href='%s' class='bs'>%s</a></h1>\n\n" % (
                    self.get_absolute_url(), self.meta['title']
                )
        ret_val += "<div class='date'>%s</div>" % (self.meta['pubdate'].strftime("%b %d %Y"),)
        return ret_val
    
    def get_absolute_url(self):
        year = self.meta['pubdate'].year
        month = self.meta['pubdate'].month
        day = self.meta['pubdate'].day
        return "/%s/%02d/%02d/%s/" % (year, month, day, self.meta['slug'])
    
    def add_meta(self, text):
        name, data = text.split(':')[0], (':'.join(text.split(':')[1:]).strip())
        self.meta[name.lower()] = data
        
    
