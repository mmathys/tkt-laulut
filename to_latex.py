#!/usr/bin/python3
from os import listdir
from os.path import isfile, join
import re
import csv

# indentation and spacing
SONG_NUMBER_SEP = "\\hspace{2pt}"
SONGTITLE_INDENT = "20pt"
SONGTITLE_PRE_SKIP = "\\vspace{5pt}"
SONGTITLE_POST_SKIP = "\\[6pt]"
VERSE_SKIP = "10pt"


def index_hack(name):
    """Hack indexing to work with åäö."""
    prefix = name
    prefix = re.sub("[åÅ]", "zza", prefix, re.U)
    prefix = re.sub("[äÄ]", "zzb", prefix, re.U)
    prefix = re.sub("[öÖ]", "zzc", prefix, re.U)
    return prefix + "@" + name


def line_hack(line):
    """Replace problematic characters with latex commands."""
    line = line.replace("#", "\\#")
    line = line.replace("%", "\\%")
    line = line.replace("+", "\\texttt{+}")
    line = line.replace(";,;", ":,:")
    if line.startswith(":,:"):
        line = "\\hspace{0pt-\\widthof{:,: }}"+line
    if line: line += "\\\\"
    return line


def generate_song(data, first):
    out = []

    title = data["title"]
    melody = data["melody"]
    lyrics = data["lyrics"]
    index = data["number"]

    out.append("%")
    out.append("% " + title)
    out.append("%")

    # minipages for title+first verse and each verse to avoid bad page breaks
    out.append("\\noindent\\begin{minipage}{\\linewidth}")
    out.append(SONGTITLE_PRE_SKIP)

    # song number offset by correct amount
    out.append("\\hspace{{{2}-\\widthof{{\\large\\bf {0}.{1}}}}}{{\\large\\bf {0}.{1}}}"
        .format(index, SONG_NUMBER_SEP, SONGTITLE_INDENT))

    # song title in parbox for line wrapping
    t = "\\parbox[t]{{0.85\\linewidth}}{{\\raggedright {{\\large\\bf {}}}".format(title)
    if melody is not None:
        t += "\\\\[2pt]\\small\\emph{{{0}}}\\{1}}}".format(melody, SONGTITLE_POST_SKIP)
    else:
        t += "\\{0}}}".format(SONGTITLE_POST_SKIP) # close \leftline\parbox
    out.append(t)

    out.append("\\index{{{}}}".format(index_hack(title)))

    if not first:
        out.append("\\noindent\\begin{minipage}{\\linewidth}")
    out.append("\\begin{verse}")

    for line in lyrics.split("\n"):
        out.append("\t" + line_hack(line))

    out.append("\\end{verse}")
    out.append("\\end{minipage}\\\\[" + VERSE_SKIP + "]")

    return "\n".join(out)


def main(order_file, song_dir):
    order = []
    with open(order_file, "r") as f:
        for row in csv.reader(f):
            order.append({
                "number": row[0] if len(row[0]) > 0 else None,
                "file": row[1] + ".txt",
                "alternate_titles": row[2:]
            })

    count = 0
    data = []
    for i in order:
        with open(join(song_dir, i["file"]), "r") as f:
            lines = [l.strip() for l in f]

            if i["number"] is None:
                number = count
                count += 1
            else:
                number = i["number"]

            title = lines[0]
            melody = lines[1] if len(lines[1]) > 0 else None
            lyrics = "\n".join(list(filter(lambda s: len(s) != 0, lines[2:])))

            data.append({
                "title": title,
                "alternate_titles": i["alternate_titles"],
                "number": number,
                "melody": melody,
                "lyrics": lyrics
            })

    print(generate_song(data[0], True))
    for i in data[1:]:
        print(generate_song(i, False))

if __name__ == "__main__":
    from sys import argv
    main(argv[1], argv[2])
