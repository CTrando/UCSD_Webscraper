import bs4, os


def has_word(buffer, word):
    for sentence in buffer:
        if word in sentence:
            return True
    return False


HTML_STORAGE = 'classes'

dir = os.path.join(os.curdir, HTML_STORAGE, 'CSE')
os.chdir(dir)
buffer_buffer = [[]]
buffer = []
for root, dirs, files in os.walk(os.curdir):
    for file in files:
        with open(file) as html:
            soup = bs4.BeautifulSoup(html, 'lxml')
            for string in soup.stripped_strings:
                if 'CSE' == string:

                    if not has_word(buffer, 'Note') and '|' not in buffer and not has_word(buffer, 'Enrolled') \
                            and not has_word(buffer, 'Section'):
                        buffer_buffer.append(buffer)
                    buffer = []
                buffer.append(string)

for thing in buffer_buffer:
    print(thing)
