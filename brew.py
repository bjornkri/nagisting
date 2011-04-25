import os
import glob
import codecs

from hops.blogpost import BlogPost
import settings


def main():
    blogposts = []
    blog_index = {}
    for infile in glob.glob(os.path.join(
            settings.SOURCES['published'], '*.txt')
        ):
        file_obj = codecs.open(infile, mode="r", encoding="utf8")
        blog = BlogPost(file_obj)
        blogposts.append(blog)
        year = blog.meta['pubdate'].year
        month = blog.meta['pubdate'].month
        if not year in blog_index:
            blog_index[year] = {}
        if not month in blog_index[year]:
            blog_index[year][month] = []
        blog_index[year][month].append(blog)
        file_obj.close()
        
    index_file = ""
    blogs = sorted(blogposts, key=lambda blog: blog.meta['pubdate'], reverse=True)
    for blogpost in blogs:
        filename = "%s%s%02d%02d_%s.php" % (
                settings.SERVER_ROOT,
                blogpost.meta['pubdate'].year, 
                blogpost.meta['pubdate'].month, 
                blogpost.meta['pubdate'].day,
                blogpost.meta['slug'])
        f = open(filename, "w")
        f.write(blogpost.html)
        index_file += blogpost.html
        f.close()
    filename = settings.SERVER_ROOT + "main.php"
    f = open(filename, "w")
    f.write(index_file)
    f.close()
    print blog_index
    for year in blog_index:
        for month in blog_index[year]:
            filename = "%s%s%02d.php" % (settings.SERVER_ROOT, year, month)
            f = open(filename, "w")
            blogs = sorted(blog_index[year][month], key = lambda blog: blog.meta['pubdate'])
            for blogpost in blogs:
                f.write(blogpost.html)
            f.close()
if __name__ == "__main__":
    main()
