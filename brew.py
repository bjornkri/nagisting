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
    blog = blog.encode('utf-8')
    f.write(blog)
    f.close()
    
def write_index(posts, filename, archive=None, reverse=False):
    f = open(filename, "w")
    index = ""
    for post in posts:
        index += post.get_header() + post.html
    if archive:
        index += archive
    f.write(index)
    f.close()
    
def generate_archive(index):
    archive_html = "\n<div class='archive'>\n<h2>Archives</h2>\n<ul>\n"
    for year in sorted(index, reverse=True):
        for month in sorted(index[year], reverse=True):
            archive_date = datetime.date(year, month, 1)
            archive_line = "\t<li><a href='/%s/%02d/'>%s</a></li>\n" % (
                year, 
                month, 
                archive_date.strftime('%B %Y')
                )
            archive_html += archive_line
    return archive_html + "</ul></div>"

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
            # Temporary fix: I'm on Brussels time, which is 2 hours ahead of 
            # UTC. Proper timezone support will be added later.
            pubDate = post.meta['pubdate'] - datetime.timedelta(0,0,0,0,0,2,0),
        )
        rss_items.append(item)
    
    rss = PyRSS2Gen.RSS2(
        title = "bjornssaga.com",
        link = "http://bjornssaga.com",
        description = "Latest entries from bjornssaga.com",
        lastBuildDate = posts[0].meta['pubdate'] - datetime.timedelta(0,0,0,0,0,2,0),
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
        blog = BlogPost(infile)
        blogposts.append(blog)
        year = blog.meta['pubdate'].year
        month = blog.meta['pubdate'].month
        if not year in blog_index:
            blog_index[year] = {}
        if not month in blog_index[year]:
            blog_index[year][month] = []
        blog_index[year][month].append(blog)
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

    # Generate archive index block
    archive = generate_archive(blog_index)

    # Write month index
    for year in blog_index:
        for month in blog_index[year]:
            filename = "%s%s%02d.php" % (settings.SERVER_ROOT, year, month)
            blogs_by_month = sorted(blog_index[year][month], key = lambda blog: blog.meta['pubdate'])
            write_index(blogs_by_month, filename, archive)

    # Write RSS
    write_rss(blogs[:10], "%sfeed.rss" % settings.SERVER_ROOT)

    # Write main index
    filename = settings.SERVER_ROOT + "main.php"
    write_index(blogs[:20], filename, archive, True)
    
if __name__ == "__main__":
    main()
