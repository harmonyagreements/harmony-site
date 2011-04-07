#!/usr/bin/python

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

def extract_text(filename):
    handle = open(filename, 'r')
    lines = handle.readlines()
    return lines

def table_header():
    html = """<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Harmony Agreements</title>
<link href="styles.css?m=1302184351" rel="stylesheet" type="text/css">
<link rel="shortcut icon" href="images/favicon.ico">
</head>
<body>
<div class="comments">
<table>
"""
    return html
    
def table_comments(comments):
    html = "\n"
    for comment in comments:
        html += '<div class="bubble"><strong>'
        html += comment['tag']
        html += ': </strong>'
        html += comment['text']
        html += '</div>' + "\n"
    return html
    
    
def table_row(index, line, comments):
    html = '<tr><td class="lineno">'+str(index)+'</td>'
    html += '<td class="line">'+line+'</td>'
    html += '<td>'
    if index in comments:
        html += table_comments(comments[index])
    html += '</td></tr>' + "\n"
    return html

def table_footer():
    html = """</table>
</div>
</body>
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-22549809-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</html>
"""
    return html

def write_html(filename, text, comments):
    index = 0
    html = table_header()
    for line in text:
        index += 1
        html += table_row(index, line, comments)

    if -1 in comments:
        html += table_row(-1, '', comments)

    html += table_footer()
    output = open(filename, 'w')
    output.write(html)
    output.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Process comments on a text file.')
    parser.add_argument('text', metavar='TEXT',
            help='A plain text file to be marked up with comments.')
    parser.add_argument('--comments', metavar='COMMENTS', default='./',
            help='A path to the directory containing comment files.')
    parser.add_argument('--out', metavar='OUTFILE', default='comments.html',
            help='Where to write the output.')
    args = parser.parse_args()

    comments = extract_comments(args.comments)
    text = extract_text(args.text)
    write_html(args.out, text, comments)
