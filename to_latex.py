#!/usr/bin/python3
from os import listdir
from os.path import isfile, join
import re

songfiles = sorted([join("songs", f) for f in listdir("songs") if isfile(join("songs", f))])

# indentation and spacing
SONG_NUMBER_SEP = "\\hspace{2pt}"
SONGTITLE_INDENT = "20pt"
SONGTITLE_PRE_SKIP = "\\vspace{5pt}"
SONGTITLE_POST_SKIP = "\\[6pt]"
VERSE_SKIP = "10pt"

# hack indexing to work with åäö
def indexhack(name):
	prefix = name
	prefix = re.sub("[åÅ]", "zza", prefix, re.U)
	prefix = re.sub("[äÄ]", "zzb", prefix, re.U)
	prefix = re.sub("[öÖ]", "zzc", prefix, re.U)
	return prefix + "@" + name

# replace problematic characters with latex commands
def linehack(line):
	line = line.replace("#", "\\#")
	line = line.replace("%", "\\%")
	line = line.replace("+", "\\texttt{+}")
	line = line.replace(";,;", ":,:")
	if line.startswith(":,:"):
		line = "\\hspace{0pt-\\widthof{:,: }}"+line
	if line: line += "\\\\"
	return line

# hack for inconsistent data
def melodyhack(line):
	line = line.replace("Sävel: ", "")
	return line

index = 0
for f in songfiles:
	with open(f, 'r') as songfile:
		lines = [l.strip() for l in songfile]
		text = "\n".join(lines)

		m = re.search("\{.*\}", text, re.M | re.DOTALL)
		if (m): 
			text = text.replace(m.group(0), "")
		lines = text.split("\n")

		title = lines[0]
		melody = lines[1]

		print("%")
		print("% " + title)
		print("%")
		# minipages for title+first verse and each verse to avoid bad page breaks
		print("\\noindent\\begin{minipage}{\\linewidth}")
		print(SONGTITLE_PRE_SKIP)
		# song number offset by correct amount 
		print("\\hspace{{{2}-\\widthof{{\\large\\bf {0}.{1}}}}}{{\\large\\bf {0}.{1}}}".format(index, SONG_NUMBER_SEP, SONGTITLE_INDENT))
		# song title in parbox for line wrapping
		print("\\parbox[t]{{0.85\\linewidth}}{{\\raggedright {{\\large\\bf {}}}".format(title),end='')
		if (melody):
			print("\\\\[2pt]\\small\\emph{{{0}}}\\{1}}}".format(melodyhack(melody), SONGTITLE_POST_SKIP))
		else:
			print("\\{0}}}".format(SONGTITLE_POST_SKIP)) # close \leftline\parbox

		index += 1
		print("\\index{{{}}}".format(indexhack(title)))		

		verses = ("\n".join(lines[2:])).strip().split("\n\n")
		first = True
		for verse in verses:
			verse = verse.split("\n")
			if not first:
				print("\\noindent\\begin{minipage}{\\linewidth}")
			else:
				first = False
			print("\\begin{verse}")
			for line in verse:
				print("\t"+linehack(line))
			print("\\end{verse}")
			print("\\end{minipage}\\\\["+VERSE_SKIP+"]")
