import urllib, urllib2, cookielib
import re
import string
import sys
import yaml
from BeautifulSoup import BeautifulSoup
from unbuffered import Unbuffered
from freq import frequency
from getpass import getpass

baseurl = "https://evaluations-uchicago-edu.proxy.uchicago.edu/evaluation.cfm?fk_olcourseid={0}"


print "CNET ID:",
username = raw_input()
password = getpass()

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

login_data = urllib.urlencode({'username' : username, 'j_password' : password})
opener.open('https://evaluations-uchicago-edu.proxy.uchicago.edu/', login_data)

def q_and_a(xs):
    q = []
    a = []
    for x in xs:
        s = x.string
        if s is not None:
            if '?' in s:
                q += [s.strip()]
            else:
                a += [s.strip()]
    return (q,a)

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def makeEntry (idnum):
    global opener

    courseurl  = baseurl.format(idnum)
    coursepage = opener.open(courseurl).read()
    coursesoup = BeautifulSoup(coursepage)
    entrydict  = {}
    # I apologize for the hackishness of the parser
    try:
        info                   = coursesoup.span.contents[1].split()
        entrydict['dept']      = info[0].encode('ascii','ignore')
        entrydict['coursenum'] = info[1].encode('ascii','ignore')
        entrydict['avetime']   = coursesoup.findAll('strong')[2].parent.findAll('td')[5].string.encode('ascii','ignore')
        entrydict['quarter']   = coursepage.split('Quarter')[1][6:100].split('<')[0].encode('ascii','ignore')
        entrydict['teacher']   = coursesoup.findAll('b')[3].next.next[1:].encode('ascii', 'ignore')
        q_and_a                = 
        #qdict                  = {}
        #for question in questions:
        #   answer = question.next.next.next.next
    except AttributeError:
        return

    if isNum(entrydict['avetime']):
        questions              = coursesoup.p.findAll('b')

    else:
        entrydict['avetime'] = coursesoup.findAll('strong')[9].parent.findAll('td')[5].string.encode('ascii','ignore')


    # print output along with id number when:
    # - not every char in avetime is a num or '.'
    # - raise BadStatusLine(line)
    #   - depending on what this error means, the best action might be to
    #     relogin and try downloading it again

    # I ended up just printing it every time (why not?) but I should still check out that error

    return entrydict

def entryGen(start, end):
    for i in xrange(start,end):
        if i is not None:
            yield makeEntry(i)
# old starting indices
# 886
# 906
# 30429
out = open(sys.argv[1], 'w')
# set it to write after every new entry is received in case of early termination
out = Unbuffered(out)
out.write('---\n')
for e in entryGen(6636,30429):
    yamline = yaml.dump(e)
    out.write('- {0:s}'.format(yamline))
    #print yamline
out.closed
