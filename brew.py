import os
import glob
import codecs
import datetime
import PyRSS2Gen

from hops.blogpost import BlogPost
import settings

def write_blog(post, filename):
    f = open(filename, "w")
    blog = post.get_header() + post.html
    f.write(blog)
    f.close()
    
def write_index(posts, filename, reverse=False):
    f = open(filename, "w")
    index = ""
    for post in posts:
        index += post.get_header() + post.html
    f.write(index)

def write_rss(posts, filename):
    rss_items = []
    for post in posts:
        if 'link' in post.meta:
            the_link = post.meta['link']
            html = post.html + "\n\n<p><strong><a href='%s'>&beta;</a></strong></p>" % post.get_absolute_url()
        else:
            the_link = post.get_absolute_url()
            html = post.html
            
        item = PyRSS2Gen.RSSItem(
            title = post.meta['title'],
            link = the_link,
            description = html,
            pubDate = post.meta['pubdate'],
        )
        rss_items.append(item)
    
    rss = PyRSS2Gen.RSS2(
        title = "bjornssaga.com",
        link = "http://bjornssaga.com",
        description = "Latest entries from bjornssaga.com",
        lastBuildDate = datetime.datetime.utcnow(),
        items = rss_items,
    )
    
    rss_file = open(filename, "w")
    rss.write_xml(rss_file)
    rss_file.close()

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



def main():
    blogposts, blog_index = get_blogposts(settings.SOURCES['published'])
    drafts, draft_index = get_blogposts(settings.SOURCES['drafts'])

    blogs = sorted(blogposts, key=lambda blog: blog.meta['pubdate'], reverse=True)

    # Write individual blog posts
    for blogpost in blogs:
        filename = "%s%s%02d%02d_%s.php" % (
                settings.SERVER_ROOT,
                blogpost.meta['pubdate'].year, 
                blogpost.meta['pubdate'].month, 
                blogpost.meta['pubdate'].day,
                blogpost.meta['slug'])
        write_blog(blogpost, filename)

    # Write draft
    for draft in drafts:
        filename = "%sdraft_%s.php" % (
            settings.SERVER_ROOT,
            draft.meta['slug']
        )
        write_blog(draft, filename)

    # Write main index
    filename = settings.SERVER_ROOT + "main.php"
    write_index(blogs[:10], filename, True)

    # Write month index
    for year in blog_index:
        for month in blog_index[year]:
            filename = "%s%s%02d.php" % (settings.SERVER_ROOT, year, month)
            blogs = sorted(blog_index[year][month], key = lambda blog: blog.meta['pubdate'])
            write_index(blogs, filename)

    # Write RSS
    write_rss(blogs[:10], "%sfeed.rss" % settings.SERVER_ROOT)
    
    
if __name__ == "__main__":
    main()
