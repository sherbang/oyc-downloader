#!/usr/bin/env python3
import re
import sys
from robobrowser import RoboBrowser
from script_helpers.urllib import FileExistsException, download_file
from urllib.parse import urljoin


def get_mp3_url(lecture_url):
    browser = RoboBrowser()
    browser.open(lecture_url)

    return browser.get_link(href=re.compile('\\.mp3$'))['href']


if __name__ == '__main__':
    sessions_page = sys.argv[1]

    browser = RoboBrowser()
    browser.open(sessions_page)

    lecture_links = browser.get_links(href=re.compile('lecture-'))

    for link in lecture_links:
        lecture_url = link['href']
        # ensure absolute url:
        lecture_url = urljoin(sessions_page, lecture_url)

        mp3_url = get_mp3_url(lecture_url)

        try:
            filename = download_file(mp3_url)
            print('Downloaded {}'.format(filename))
        except FileExistsException as exc:
            filename = exc.filename
            print('File ({}) already exists - skipped'.format(filename))
