

from PyQt5.QtCore import QSettings
import logging
import mwclient
import os
from datetime import datetime
logger = logging.getLogger('LabJournal')


APPLICATION_NAME='foo'
COMPANY_NAME='foo'

bot_username = 'test'      # username
bot_password = 'testtest'  # password


class MediaWikiHandler:
    """
    Hanlder for the MediaWiki
    """

    def __init__(self):

        settings = QSettings(APPLICATION_NAME, COMPANY_NAME)
        mediawiki_address = settings.value('MediaWiki/host', 'localhost')  # address of the server of the MediaWiki
        mediawiki_protocol = settings.value('MediaWiki/protocol', 'http')  # protocol (http or https)
        mediawiki_path = '/{}/'.format(settings.value('MediaWiki/path', 'mediawiki'))  # path to MediaWiki after address
        del settings

        self.template_folder = os.path.join(os.path.dirname(__file__),'templates')

        # Initialize the Site object
        self.site = mwclient.Site((mediawiki_protocol, mediawiki_address), mediawiki_path)  # connect
        self.site.login(bot_username, bot_password)  # optional, if login is required

    def get_labjournal_pages(self,mode='prefix',text='MK'):
        """

        Parameters
        ----------
        mode : {'prefix', 'category'}
            Mode how to get the pages. (Default is 'prefix')
        text : str, optional
            Text used to filter the entries for. Dependend on the mode, it is the prefix or category name.

        Returns
        -------
        list_pages : list(str)
            Returns a list of page names matching the conditions

        Raises
        ------
        NotImplementedError
            if mode is not implemented
        """

        if mode == 'prefix':
            list_pages = list(self.site.allpages(prefix=text))
        else:  # raise a warning if mode not implemented
            raise NotImplementedError("mode = '{}' is not implemented yet")

        return list_pages

    def parse_header(self,page):
        """
        get the infos from the MediaWiki header
        Parameters
        ----------
        page : mwclient.Page
            Page to analyse
        Returns
        -------

        """

    def create_new_labjournal_entry(self,name,**kwargs):
        """

        Parameters
        ----------
        name : str
            Name of the MediaWiki page
        kwargs : dict, optional
            category : str or list(str)
                adds categories to the header of the page
            simid : str
                uses `simid` for XXX_ID in the template (Default is `name`.)
            folder : str
                uses `folder` for XXX_FOLDER in the template
            date : str
                uses `date` for XXX_DATE in the template, `date`='auto' will use the current date
            description : str
                uses `description` for XXX_DESCRIPTION in the template
            details : str
                uses `details` for XXX_DETAILS in the template

        Returns
        -------

        """
        page = self.site.pages[name]  # create the Page object

        # load the content of the template
        with open(os.path.join(self.template_folder,'labjournal_header.txt'), 'r') as fp:
            content = fp.read()

        # handling of keywords
        index_toc = content.index('__TOC__')  # get the index where __TOC__ begins
        if 'category' in kwargs.keys():  # Add categories
            if type(kwargs['category']) in [list, tuple]:
                for category in kwargs['category']:
                    category = category[0].upper() + category[1:]
                    content = content[:index_toc-1] + "[[Category:{}]]\n".format(category) + content[index_toc-1:]
            else:
                category = kwargs['category']
                category = category[0].upper() + category[1:]
                content = content[:index_toc - 1] + "[[Category:{}]]\n".format(category) + content[index_toc - 1:]

        if 'simid' in kwargs.keys():  # fill in the ID if given
            content = content.replace('XXX_ID', kwargs['simd'])
        else:  # fall back to the name of the page
            content = content.replace('XXX_ID', name)  # replace the ID by the pagename

        if 'folder' in kwargs.keys():  # fill in the folder if given
            content = content.replace('XXX_FOLDER', kwargs['folder'])

        if 'date' in kwargs.keys():  # fill in the date is given
            if kwargs['date'] == 'auto':  # take current date if set to 'auto'
                time = datetime.now()
                content = content.replace('XXX_DATE', '{:02d}.{:02d}.{}'.format(time.day,time.month,time.year))
            else:
                content = content.replace('XXX_DATE', kwargs['date'])

        if 'description' in kwargs.keys():  # fill in the Description if given
            content = content.replace('XXX_DESCRIPTION', kwargs['description'])

        if 'details' in kwargs.keys():  # fill in the Details if given
            content = content.replace('XXX_DETAILS', kwargs['details'])

        # create a new page
        if not page.exists or 'force' in kwargs.keys() and kwargs['force']:
            page.save(content, summary="automatically initiated")  # save the text to the page


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    mw = MediaWikiHandler()
    #print mw.get_labjournal_pages('prefix', 'LAMMPS')
    mw.create_new_labjournal_entry('MK0002',
                                   folder='test',
                                   date='auto',
                                   description='New: Awesome: page',
                                   details='* more info\n* even more\n* most',
                                   category=['test','LAMMPS'],
                                   force=True)