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
        if current_line == "--------":
            current_line = self.file_obj.readline().strip()
            while not current_line == "--------":
                self.add_meta(current_line)
                current_line = self.file_obj.readline().strip()
        else:
            self.text = current_line
        for current_line in self.file_obj:
            self.text += current_line
        
        self.html = markdown.markdown(self.text)
        
    
    def add_meta(self, text):
        name, data = text.split(':')[0], (':'.join(text.split(':')[1:]).strip())
        self.meta[name.lower()] = data
        
    