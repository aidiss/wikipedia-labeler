"""Creates persons interest map"""
import json
import random
import sys

import lxml.html
import requests


def load_word(word='data'):
    """Load a wikipedia page"""
    host = 'https://en.wikipedia.org/wiki/'
    r = requests.get(host + word)
    html = lxml.html.fromstring(r.text)
    urls = html.xpath('//a/@href')
    urls = [x for x in urls if x.startswith('/wiki/')]
    urls = [x for x in urls if ':' not in x]
    urls = set(urls)
    urls.remove('/wiki/Main_Page')
    keywords = [x[6:] for x in urls]
    return keywords


def get_assessment(keyword):
    """Gets player inputs on two questions"""
    d = {}
    while True:
        try:
            d['knowledge'] = int(
                input('How much do you know about this topic?\n'))
            d['interest'] = int(input('How much would you like to know?\n'))
            break
        except ValueError as _:
            print('Please enter an integer!')
            if input('Would you like to quit'):
                with open(f'data/{username}.json', 'w') as f:
                    json.dump(db, f, indent=2)
                sys.exit()
            continue
    return d


def load_db(username):
    try:
        with open(f'data/{username}.json', 'r') as f:
            db = json.load(f)
            return db
    except Exception as e:
        print(e)
        return {}


def get_persons_opinion(word):
    print('What about word %s' % word)
    assessment = get_assessment(word)
    return assessment


def choose_words_for_a_person(db, person):
    """Chooses words for a person"""
    person_words = db
    words_not_assessed = [x for x in person_words if not x]
    chosen_words = random.sample(words_not_assessed, 5)
    return chosen_words


def get_follow_up_words(word):
    return load_word(word)


def main():
    print('Welcome to the place!')
    print('Would you like to start')
    global username
    username = input('What is your name?')
    global db
    db = load_db(username)
    word = input('Enter a simple word\n')
    word = word.replace(' ', '_')

    print('You chose', word)
    more_words = load_word(word)
    words = random.sample(more_words, 2)
    for word in words:
        opinion = get_persons_opinion(word)

        if opinion['interest'] > 3:
            words.extend(get_follow_up_words(word))
        db[word] = opinion

    print(db)


if __name__ == "__main__":
    main()
