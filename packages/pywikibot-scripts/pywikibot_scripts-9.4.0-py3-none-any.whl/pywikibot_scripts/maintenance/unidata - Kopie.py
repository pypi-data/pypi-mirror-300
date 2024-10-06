"""Run this module multiple times using different python versions.

Note: I seems that running under the latest version of Python (3.7) gives a
superset of the older version and should be enough. But I have not tested this
completely.
"""
from functools import cache
from json import dump, dumps, load
from queue import Queue
from re import findall
from sys import maxunicode
from threading import Thread

from pywikibot import Site
from pywikibot.comms.http import session
from pywikibot.family import Family
from scripts.maintenance.wikimedia_sites import families_list

NUMBER_OF_THREADS = 26
FILEPATH = '/data/firstup_excepts.json'


@cache
def chars_uppers_wikilinks():
    n = 0
    chars = []
    uppers = []
    wikilinks = ''
    for i in range(0, maxunicode + 1):
        c = chr(i)
        uc = c.upper()
        if uc != c:
            n += 1
            chars.append(c)
            uppers.append(uc)
            # MediaWiki is first-letter case
            wikilinks += '[[MediaWiki:' + c + ']]\n'
    return chars, uppers, wikilinks


def escape(c):
    ch = ord(c)
    return (r'\x%02x' % ch if ch <= 255 else r'\u%04x' %
            ch if ch <= 65535 else r'\U%08x' % ch)


def process_site(fam_name, site_code):
    print(f'processing {site_code}.{fam_name}...')
    site_excepts = {}
    try:
        j = session.post(
            'https://{site_code}.{fam_name}.org/w/api.php?'
            'action=parse&contentmodel=wikitext&prop=text'
            '&format=json&utf8'.format_map(locals()),
            data={
                'text': wikilinks
            },
            timeout=10,
        ).json()
    except Exception as e:
        print(e)
    else:
        pased_text = j["parse"]["text"]['*']
        titles = findall(r'title="[^:]*:(.)', pased_text)
        for i, original_char in enumerate(chars):
            title_char = titles[i]
            if uppers[i] != title_char:
                site_excepts[escape(original_char)] = escape(title_char)
    print(f'processing {site_code}.{fam_name} done.')
    return site_excepts


def threads_target(q):
    while True:
        try:
            fam, code = q.get()
        except TypeError:  # non-iterable NoneType object
            break
        site_excepts = process_site(fam, code)
        families_excepts[fam].setdefault(code, {}).update(site_excepts)
        q.task_done()


def spawn_threads(q):
    threads = []
    for i in range(NUMBER_OF_THREADS):
        t = Thread(target=threads_target, args=(q, ))
        t.start()
        threads.append(t)
    return threads


def stop_threads(q, threads):
    for i in range(NUMBER_OF_THREADS):
        q.put(None)
    for t in threads:
        t.join()


def main():
    q = Queue()
    threads = spawn_threads(q)
    for fam_name in families_list:
        family = Family.load(fam_name)
        families_excepts.setdefault(fam_name, {})
        for site_code in family.languages_by_size:
            site = Site(site_code, family)
            if site.namespaces[8].case != 'first-letter':
                raise ValueError('MW namespace case is not first-letter')
            fam_code = (fam_name, site_code)
            if fam_code in {
                ('wikisource', 'www'),
                ('wikisource', 'mul'),
                ('wikiversity', 'test'),
            }:
                continue  # the API of these codes does not respond as expected
            q.put(fam_code)
    # block until all tasks are done
    q.join()
    stop_threads(q, threads)


def save_json(obj, path):
    with open(path, 'w', encoding='utf8') as f:
        try:
            dump(obj, f)
        except TypeError:  # Python 2 TypeError: must be unicode, not str
            f.write(unicode(dumps(obj)))


def load_json(path):
    try:
        with open(path, encoding='utf8') as f:
            return load(f)
    except OSError:
        print('File not found:', path)
        return {}


def run():
    global families_excepts, chars, uppers, wikilinks
    chars, uppers, wikilinks = chars_uppers_wikilinks()
    save_json({
        'chars': chars,
        'uppers': uppers,
        'wikilinks': wikilinks
    }, 'user-temp-save.json')
    j = load_json('user-temp-save.json')
    chars, uppers, wikilinks = j['chars'], j['uppers'], j['wikilinks']
    #    families_excepts = load_json(FILEPATH)
    families_excepts = {}
    main()
    save_json(families_excepts, FILEPATH)
    print(process_site('wiktionary', 'fr'))


if __name__ == '__main__':
    run()
