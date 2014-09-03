---
layout: post
title: Obligatory Metablog post
comments: True
---

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

    {% include comments.html %}
    
to default.html . I then added a new comments.html file to _includes with these contents:
 
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

Note that this is exactly what Disqus suggested I should add, bracketed by the if statements Joshua recomments. To include comments in a post, I then add 

    comments: True
    
to the metadata header in the markdown.

# Formatting code in the blog that tries to do tricks with html includes dammit

# Set up the URL with Godaddy



# Google Analyitics

Needs URL set up