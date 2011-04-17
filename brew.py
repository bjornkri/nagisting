import os
import glob
import codecs

from hops.blogpost import BlogPost
import settings


def main():
    blogposts = []
    for infile in glob.glob(os.path.join(
            settings.SOURCES['published'], '*.txt')
        ):
        file_obj = codecs.open(infile, mode="r", encoding="utf8")
        blogposts.append(BlogPost(file_obj))
        file_obj.close()
        
    index_file = ""
    for blogpost in blogposts:
        filename = "%s%s_%s.php" % (
                settings.SERVER_ROOT,
                blogpost.meta['pubdate'],
                blogpost.meta['slug'])
        f = open(filename, "w")
        f.write(blogpost.html)
        index_file += blogpost.html
        f.close()
    filename = settings.SERVER_ROOT + "main.php"
    f = open(filename, "w")
    f.write(index_file)
    f.close()

if __name__ == "__main__":
    main()