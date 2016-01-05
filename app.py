import cookielib
import mechanize
import praw
import sys
import time

def generate_username():
    # in the future i should make this automatically generate usernames from a dictionary file or something
    return raw_input("Username: ")

def generate_comment(username):
    # returns the text to be commented onto the post. this example just comments the username onto the post.
    return username

def create_reddit_account(username, password, br, cj):
    # set up the browser object
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Chrome')]

    # navigate to the registration page and register
    br.open('https://www.reddit.com/register')
    br.form = list(br.forms())[0]
    br.form['user'] = username
    br.form['passwd'] = password
    br.form['passwd2'] = password
    br.submit()

    print 'user account created'

    return

def post_comment(username, password, url):
    # create a new praw object to log us into reddit
    r = praw.Reddit(user_agent='Chrome')
    r.login(username, password, disable_warning=True)

    # get the proper submission based off the url provided
    submission = r.get_submission(url=url)

    # comment with whatever text you need in the comment
    submission.add_comment(generate_comment(username))

    return

def main(password, url):
    while True:
        # request a new username
        username = generate_username()

        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()

        # create a reddit account with those credentials
        create_reddit_account(username, password, br, cj)

        # post a comment with that new account
        post_comment(username, password, url)

        # rest for 10 minutes
        time.sleep(10 * 60)

if __name__ == '__main__':
    # format is password, url
    password = sys.argv[1]
    url = sys.argv[2]
    main(password, url)