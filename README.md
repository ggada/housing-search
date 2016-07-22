# housing-search

This uses the facebook graph API to incrementally mail out udub house listings from group id 385662361445807 (this is an open housing group within a closed UW group). I've filtered the words "sublet", "female" and "girl" out to avoid sublet/females only/girls only posts. This can be customized to your taste. The mail consists of a neat little table with UTC post timestamp, post text and facebook deeplinks so it opens the post directly in the facebook app on both mobile (use mob) and desktop (use FBL).

##To make it work:

###1. Install python libraries:
* jinja2
* requests
* ipdb (dubugging only)

###2. Setup environment variables:
```
FB_API # you need an FB API token to make this work
FROM_EMAIL
FROM_EMAIL_PASS
TO_EMAIL
```

###3. Cron it

###4. Profit??!

Although this uses some hardcoding, I'm sure this logic can be extended to arbitrary facebook groups and with arbitrary filtering requirements. Now on to finding myself a perfect house.....
