---
layout: post
title: Obligatory Metablog Post
comments: True
---

Everyone who writes a blog should have an entry like this, so that others can learn what worked and what didn't. My blog is hosted on GitHub, and I pretty much followed their [guide](https://pages.github.com/). 

# Why jekyll? Isn't that Ruby? 

I started the blog with jekyll's clean start

    > jekyll new blog
    
and edited files from there.

# run jekyll with -w to rebuild the site in a loop

# .gitignore



# Comments

I used [Joshua Lande's blog post](http://joshualande.com/jekyll-github-pages-poole/) as a rough guide to get Disqus comments set up. This was pretty easy.

TODO fix formatting

I added
 
    {% raw %}
    {% include comments.html %}
    {% endraw %}
    
to default.html . I then added a new comments.html file to _includes with these contents:
 
    {% raw %}
    {% if page.comments %}
     <div id="disqus_thread"></div>
     <script type="text/javascript">
             /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
             var disqus_shortname = 'intuitivecounter'; // required: replace example with your forum shortname
     
             /* * * DON'T EDIT BELOW THIS LINE * * */
             (function() {
                 var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
                 dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
                 (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
             })();
         </script>
     <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
     <a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
    {% endif %}
    {% endraw %}

Note that this is exactly what Disqus suggested I should add, bracketed by the if statements Joshua recomments. To include comments in a post, I then add 

    comments: True
    
to the metadata header in the markdown.

# Set up the URL with GoDaddy

Setting up forwarding from GoDaddy was pretty easy, even though they change their interface every five months. Sign in, pick the header's Domains menu, Manage Domains, walend.net, Manage, Add Subdomain blob.walend.net and www.blog.walend.net, and forward them to http://dwalend.github.io/blog/ , with masking. The masking is a pain, because I had to put in a list of keywords, for both forwarding entries, that I'll have to keep up-to-date at GoDaddy. I'll have to revisit that someday. 


# Google Analyitics

Needs URL set up. Looks like that will be easy, so I added google_analyitics.html and put the   {% include google_analytics.html %} line in default.html

Hard to tell if it is working or not without publishing the blog.

# Formatting code in the blog that tries to do tricks with html includes dammit


    {% raw %}
    {% raw %}
    Liquid code I don't want interpreted on the server
    {% end raw %}
    {% endraw %}

But it's really endraw, without the space. And that's why I do mostly back-end work.
