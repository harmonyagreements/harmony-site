#i!/usr/bin/python

import os, re, argparse

line_pattern = re.compile('^(?P<tag>line[s]?\s+(?P<start>\d+)(-(?P<end>\d+))?)')

def save_comment(storage, comment):
    index = int(comment['start'])
    comment['text'] = comment['text'].strip()
    if (index in storage):
        storage[index].append(comment)
    else:
        storage[index] = [comment]
    
# Extract all the comments from the comment files.
def extract_comments(path):
    files = os.listdir(path)
    storage = {}
    for filename in files:
        handle = open(path+'/'+filename, 'r')
        lines = handle.readlines()
        in_comment = 0
        start_comment = 0
        comment = {}
        for line in lines:
            # Starting a new comment
            if not in_comment and (line == '====\n'):
                in_comment = 1
                start_comment = 1
                comment = {}

            # The first line of the comment should be a line number for the text document.
            elif in_comment and start_comment:
                match = line_pattern.match(line)
                if match:
                    comment['tag'] = match.group('tag')
                    comment['start'] = match.group('start')
                    comment['end'] = match.group('end')
                    comment['text'] = ''
                else:
                    comment['tag'] = 'unknown'
                    comment['start'] = '-1'
                    comment['text'] = line 
                start_comment = 0

            # Ending the comment if we're already in one.
            elif in_comment and (line == '====\n'):
                in_comment = 0
                start_comment = 0
                save_comment(storage, comment)

            # Anything else inside the comment is text to save.
            elif in_comment:
                comment['text'] += line

    return storage


def process_comments(text, comment_dir):
    comments = extract_comments(comment_dir)
    print comments
    #print comments[20]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Process comments on a text file.')
    parser.add_argument('--text', metavar='TEXT',
            help='A plain text file to be marked up with comments.')
    parser.add_argument('--comments', metavar='COMMENTS',
            help='A path to the directory containing comment files.')
    args = parser.parse_args()
    print args
    process_comments(args.text, args.comments)
