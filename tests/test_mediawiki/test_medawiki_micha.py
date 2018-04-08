#!/usr/bin/env python
"""
Test mwclient to access the MediaWiki and Change folders

Setup for local MediaWiki on micha's laptop.

Todo:
    We should create a test MediaWiki somewhere in the group

Requirements:
    pip install mwclient
"""

import mwclient

mediawiki_address = 'localhost'  # address of the server of the MediaWiki
mediawiki_protocol = 'http'      # protocol (http or https)
mediawiki_path = '/mediawiki/'   # path to MediaWiki after address

bot_username = 'test'      # username
bot_password = 'testtest'  # password

# Initialize the Site object
site = mwclient.Site((mediawiki_protocol, mediawiki_address), mediawiki_path)  # connect
site.login(bot_username,bot_password) # optional, if login is required

# Show all sites
for page in site.allpages():
    print page.name

# Show all sites starting with LAMMPS
for page in site.allpages(prefix='LAMMPS'):
    print page.name


page = site.pages['LAMMPS']
print page.text()


print "-"*80

simid = 'MK0001'
page = site.pages[simid]

# Try to delete a page
if page.exists:  # check if page exist
    try:
        page.delete(reason='Testpurpose')  # delete page if exits
    except mwclient.errors.InsufficientPermission:
        print "I dont have the permissions to delete the page: " + page.page_title

# create a new page
if not page.exists:
    print "Pages missing: " + page.page_title
    page.save('YEAH new site', summary="automatically initiated") # save the text to the page
    page = site.pages[page.page_title]  # reload the page content of us
    print "Created page: " + page.page_title

# rewrite everything
print "rewrite page: " + page.page_title
page.save('__TOC__\n[[Category:labjournal]]\nYEAH new site', summary="automatically initiated") # save the text to the page
page = site.pages[page.page_title]  # reload the page content of us

# modify the page further
print "modify page: " + page.page_title
text = page.text()  # get the page content
page.save(text + u'\n==New Section==\nTest', summary="i should be shown in history", bot=False)
page = site.pages[page.page_title]  # reload the page content of us

# show the content
text = page.text()  # get the page content
print '-'*80 + '\nContent of Page: ' + page.page_title + '\n' + '-'*40
print  text
print '-'*80


STR_ADD=u"""
=test=
==test_1==
===test_2===
====test_2_2====
===test_3===
"""
text = page.text()  # get the page content
page.save(text+STR_ADD)
page = site.pages[page.page_title]  # reload the page content of us
