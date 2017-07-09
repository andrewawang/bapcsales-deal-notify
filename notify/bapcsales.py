import praw
import time
from datetime import datetime
import winsound
#import threading
#import smtplib
#from email.mime.text import MIMEText
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText

"""
Todo:

Add filters
Twitter bot

"""
#input your own account API token info
reddit = praw.Reddit(client_id='___________',
                     client_secret="____________",
                     refresh_token="____________",
                     password="__________",
                     user_agent="__________",
                     username="__________")

subreddit = reddit.subreddit('buildapcsales')
#new_post=next(subreddit.new())bapcsales.py
cache={} #submission id:karma count

def old_checker(post1,post2):
    """
    returns true if submission is posted already
    """
    return post1==post2

def good_deal_check(post):
    """
    returns True if a good deal
    """
    #if downvotes>1:
    #    return False
    score=post.score
    ratio=post.upvote_ratio

    #if post.link_flair_text='Out Of Stock' or post.over_18==True:
    #    return False

    if score>2 or (ratio>0.5 and age(post)>150):
        return True
    return False

def notification(post):
    """
    Notifies user of good deal.

    ToDo:
    email, text, popup notifications
    """
    local_notification(post)

    """
    score=post.score
    ratio=post.upvote_ratio
    cache[post.id]=score
    title=post.title
    #SEND EMAIL,TEXT,POPUP
    winsound.Beep(2500,1000)
    print('reddit.com'+post.permalink)
    print(price_scrubber(title)+ ' || '+title)
    print('karma count: '+str(score) + ' || upvote %: ' +str(int(ratio*100)))
    print(post.url)
    print('----------------------------------------------------------------')
    """


def email_notification(post):

    def sendemail(from_addr,
                to_addr_list,
                cc_addr_list,
                subject,
                message,
                login,
                password,
                smtpserver='smtp.gmail.com:587'):
              #http://rosettacode.org/wiki/Send_email#Python
        header  = 'From: %s\n' % from_addr
        header += 'To: %s\n' % ','.join(to_addr_list)
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        message = header + message

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login,password)
        problems = server.sendmail(from_addr, to_addr_list, message)
        server.quit()
        return problems

    sendemail(from_addr    = 'python@RC.net',
          to_addr_list = ['RC@gmail.com'],
          cc_addr_list = ['RC@xx.co.uk'],
          subject      = 'Howdy',
          message      = 'Howdy from a python function',
          login        = 'pythonuser',
          password     = 'XXXXX')

def local_notification(post):
    score=post.score
    ratio=post.upvote_ratio
    cache[post.id]=score
    title=post.title
    winsound.Beep(2500,1000)
    print('reddit.com'+post.permalink)
    print(price_scrubber(title)+ ' || '+title)
    print('karma count: '+str(score) + ' || upvote %: ' +str(int(ratio*100)))
    print(post.url)
    print('----------------------------------------------------------------')

def price_scrubber(title):
    """
    scrubs title for price
    """
    dollar_position=title.index('$')
    title=title[dollar_position:]
    end=title.find(' ')
    return title[:end]

def get_date(post):
    """
    gets UTC time of post
    """
    time = post.created#_utc
    return datetime.fromtimestamp(time)

def time_up(post):
    """
    returns True if post is roughly older than an hour, returns False if less than hour
    """
    curr_time=datetime.utcnow()
    post_time=get_date(post)
    age=(curr_time-post_time).total_seconds()
    """
    curr_time: 5:01
    post_time: 4:59
    """
    if age>3600:
        if post.id in cache:
            cache.pop(post.id)
        return True
    return False

def age(post):
    curr_time=datetime.utcnow()
    post_time=get_date(post)
    return (curr_time-post_time).total_seconds()
"""
if time_up(new_post):
    break
"""

#new_post=next(subreddit.new())
def scanner():
    refresh=subreddit.new()
    curr=next(refresh)

    n=1
    while not time_up(curr):
        print("scanner instance loop count: "+str(n))
        n+=1
        curr_id=curr.id

        if curr_id in cache:
            if curr.score-cache[curr_id]>2 and curr.score>2 and not (post.link_flair_text='Out Of Stock' or post.over_18==True):
                notification(curr)
        elif good_deal_check(curr):
            if curr_id not in cache or cache[curr_id]<curr.score:
                notification(curr)


        #notification(curr)
        curr=next(refresh)


def sales():
    n=1
    while True:

        print("sales loop count: "+str(n))
        n+=1

        scanner()
        time.sleep(60)





sales()

def sale_finder():

    while True:
        new_post=next(subreddit.new())
        if new_post.id not in cache:
            sale_finder_instance(new_post)
            #post_thread = threading.Thread(target=sale_finder_instance, args=new_post)
            #post_thread.start()
        time.sleep(30)
        """
        old_post=new_post
        new_post=next(subreddit.new())
        if not old_checker(old_post,new_post):
            sale_finder_instance(new_post)
        """

class newpost:
    def __init__(self):
        self.new_post=next(subreddit.new())
    def __iter__(self):
        return self
    def next(self):
        while True:
            old_post=self.new_post
            self.new_post=next(subreddit.new())
            if self.new_post==old_post:
                time.sleep(30)
            else:
                return self.new_post



def sale_finder_instance(post):
    #new_post=next(subreddit.new())
    while True:#time_up(post)==False: #TIMER ALGORITHM NEEDS TO BE CHANGED
        """
        Infinite loop that checks for deals every x seconds


        """
        #old_post=new_post
        #new_post=next(subreddit.new())

        #if old_checker(post,new_post):
        #    time.sleep(30) #wait x seconds before checking again

        #downvotes=new_post.downs
        #upvotes=new_post.ups
        score=post.score
        ratio=post.upvote_ratio
        #karma=upvotes-downvotes

        pid=post.id

        if pid in cache:
            if score-cache[pid]>2 and score>0:
                notification(post)
        elif good_deal_check(post):
            if pid not in cache or cache[pid]<score:
                notification(post)

        time.sleep(30) #wait x seconds before checking again



#sale_finder()

"""
Reddit Post's Functions
['STR_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_comments', '_comments_by_id', '_fetch', '_fetched', '_flair', '_info_params', '_info_path', '_mod', '_reddit', '_reset_attributes', '_safely_add_arguments', '_vote', 'approved_by', 'archived', 'author', 'author_flair_css_class', 'author_flair_text', 'banned_by', 'brand_safe', 'can_gild', 'clear_vote', 'clicked', 'comment_limit', 'comment_sort', 'comments', 'contest_mode', 'created', 'created_utc', 'delete', 'distinguished', 'domain', 'downs', 'downvote', 'duplicates', 'edit', 'edited', 'flair', 'fullname', 'gild', 'gilded', 'hidden', 'hide', 'hide_score', 'id', 'id_from_url', 'is_self', 'likes', 'link_flair_css_class', 'link_flair_text', 'locked', 'media', 'media_embed', 'mod', 'mod_reports', 'name', 'num_comments', 'num_reports', 'over_18', 'parse', 'permalink', 'post_hint', 'preview', 'quarantine', 'removal_reason', 'reply', 'report', 'report_reasons', 'save', 'saved', 'score', 'secure_media', 'secure_media_embed', 'selftext', 'selftext_html', 'shortlink', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_type', 'suggested_sort', 'thumbnail', 'thumbnail_height', 'thumbnail_width', 'title', 'unhide', 'unsave', 'ups', 'upvote', 'upvote_ratio', 'url', 'user_reports', 'view_count', 'visited']
"""
