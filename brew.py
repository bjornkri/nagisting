import os
import glob
import codecs
import datetime
import PyRSS2Gen

from hops.blogpost import BlogPost
import settings


def main():
    blogposts, blog_index = get_blogposts(settings.SOURCES['published'])
    drafts, draft_index = get_blogposts(settings.SOURCES['drafts'])
    
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
        f.write(blogpost.get_header())
        f.write(blogpost.html)
        index_file += blogpost.get_header()
        index_file += blogpost.html
        f.close()
    
    for draft in drafts:
        filename = "%sdraft_%s.php" % (
            settings.SERVER_ROOT,
            draft.meta['slug']
        )
        f = open(filename, "w")
        f.write(draft.get_header())
        f.write(draft.html)
        f.close()
    
    filename = settings.SERVER_ROOT + "main.php"
    f = open(filename, "w")
    f.write(index_file)
    f.close()
    for year in blog_index:
        for month in blog_index[year]:
            filename = "%s%s%02d.php" % (settings.SERVER_ROOT, year, month)
            f = open(filename, "w")
            blogs = sorted(blog_index[year][month], key = lambda blog: blog.meta['pubdate'])
            for blogpost in blogs:
                f.write(blogpost.get_header())
                f.write(blogpost.html)
            f.close()

    # Make RSS
    rss_items = []
    for blog in blogs[:10]:
        if 'link' in blog.meta:
            the_link = blog.meta['link']
            html = blog.html + "\n\n<p><strong><a href='%s'>&beta;</a></strong></p>" % blog.get_absolute_url()
        else:
            the_link = blog.get_absolute_url()
            html = blog.html
            
        item = PyRSS2Gen.RSSItem(
            title = blog.meta['title'],
            link = the_link,
            description = html,
            pubDate = blog.meta['pubdate'],
        )
        rss_items.append(item)
    
    rss = PyRSS2Gen.RSS2(
        title = "bjornssaga.com",
        link = "http://bjornssaga.com",
        description = "Latest entries from bjornssaga.com",
        lastBuildDate = datetime.datetime.utcnow(),
        items = rss_items,
    )
    
    rss.write_xml(open("%sfeed.rss" % settings.SERVER_ROOT, "w"))

def get_blogposts(path):
    blogposts = []
    blog_index = {}
    for infile in glob.glob(os.path.join(
            path, '*.txt')
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
    return blogposts, blog_index

if __name__ == "__main__":
    main()
