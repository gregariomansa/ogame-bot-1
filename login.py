import sys
import mechanize

browser = None
nickname = 'Legor'
password = '12345'
uni_name = 'Universo 1'
lang = 'es'
uni_id = '1'
uni_url = 's%s-%s.ogame.gameforge.com' % (uni_id, lang)
base_url = 'http://%s.ogame.gameforge.com/' % lang
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'

def login():
    global browser
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_handle_refresh(False)
    browser.addheaders = [('User-agent', user_agent)]
    request = mechanize.Request(base_url)
    browser.open(request)
    browser.select_form('loginForm')
    control = browser.form.find_control('uni')
    for item in control.items:
        if item.name == uni_url:
            item.selected = True
            break
    browser.form['login'] = nickname
    browser.form['pass'] = password
    browser.submit()
    if uni_name in browser.title():
        print "Logged as %s " % nickname + "in %s" % uni_name
    else:
        print "Login error: %s" % browser.geturl()
        sys.exit(1)
