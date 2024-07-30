# hugo-tools

Small tools for websites using the Hugo blogging software

# check-markdown-files.py

A tool which checks Hugo postings for a wide range of problems.

This tool has it's own repository.

[Go here: github.com/andreasscherbaum/check-markdown-files](https://github.com/andreasscherbaum/check-markdown-files)

## find-postings-without-comment-id.py

My blog implements a comments function using Mastodon.

Details about the implementation are [available in this blog posting](https://andreas.scherbaum.la/post/2024-05-23_client-side-comments-with-mastodon-on-a-static-hugo-website/).

In order to enable the comment functionality, the posting details of the "root" Mastodon posting need to be specified, must notably the posting ID. Being human, I sometimes forget this additional step after publishing the post.

This script scans a given directory (`content/post`) and finds any `index.md` which is committed in `git` (this ignores unpublished posts) where the `comments->id` field is empty. Add this as a cron job and it will remind you when you forgot to add the id.

Usage:

```
../hugo-tools/find-postings-without-comment-id.py content/post/
```

Where `../hugo-tools/find-postings-without-comment-id.py` is the path to the script, and `content/post/` is a blog directory.

## list-categories.py / list-tags.py

The `list-categories.py` tool scans the blog posting and finds all entries under the `categories` Frontmatter. By default it lists all entries, If one of multiple parameters are specified, only matching entries will be listed.

Similarly the `list-tags.py` tool scans entries under `tags`.

## new-blog-posting.py

Opens an input window (using TKinter) and asks for a blog posting title. Then proceeds to create the blog posting using this name, and a sanitized URL.

It will add a date in front of the URL.

## add-to-gitignore.py

Specify one or multiple image files which will be added to the `.gitignore` file in the same directory. If the `.gitignore` file does not exist, it will be created.

Only files ending in `.jpg`, `.jpeg`, `.png` and `.xcf` (*Gimp* project files) will be added, every other file is ignored.

This tool is useful to quickly add image files for a blog posting which are stored in the blog posting directory, but are not supposed to appear on the website. Like original images and such.
