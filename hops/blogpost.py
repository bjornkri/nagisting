import datetime
import markdown

class BlogPost(object):

    def __init__(self, file_obj):
        super(BlogPost, self).__init__()
        self.file_obj = file_obj
        self.meta = {}
        self.text = ""
        self.html = ""
        self.parse_file()
        
    
    def parse_file(self):
        current_line = self.file_obj.readline().strip()
        # Strip possible \ufeff from the first line
        if current_line[-8:] == "--------": 
            current_line = self.file_obj.readline().strip()
            while not current_line == "--------":
                self.add_meta(current_line)
                current_line = self.file_obj.readline().strip()
        else:
            self.text = current_line
            print "No metadata in %s" % self.file_obj.name
        
        filename = self.file_obj.name.split('/')[-1]
        self.meta['slug'] = filename.split('_')[1][:-4]
        
        self.meta['pubdate'] = datetime.datetime.strptime(
            self.meta['pubdate'], '%a %b %d %H:%M:%S %Y')
        
        self.generate_header()
        
        for current_line in self.file_obj:
            self.text += current_line
        
        self.html = markdown.markdown(self.text)
        
    
    def generate_header(self):
        if 'title' in self.meta:
            if 'link' in self.meta:
                self.text = "# [%s](%s) [#](%s)\n\n" % (
                    self.meta['title'],
                    self.meta['link'],
                    self.get_absolute_url()
                )
            else:
                self.text = "# [%s](%s)\n\n" % (
                    self.meta['title'], self.get_absolute_url()
                )
        self.text += "<p class='date'>%s</p>" % (self.meta['pubdate'].strftime("%a %b %d %Y"),)
    
    def get_absolute_url(self):
        year = self.meta['pubdate'].year
        month = self.meta['pubdate'].month
        day = self.meta['pubdate'].day
        return "/%s/%02d/%02d/%s/" % (year, month, day, self.meta['slug'])
    
    def add_meta(self, text):
        name, data = text.split(':')[0], (':'.join(text.split(':')[1:]).strip())
        self.meta[name.lower()] = data
        
    
