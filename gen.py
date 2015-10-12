#!/usr/bin/env python3
if __name__ == "__main__":
    from pathlib import Path
    from jinja2 import Template

    template_text = ""
    with open("template.html") as f:
        template_text = f.read()

    songs = []

    p = Path("songs/")
    ls = list(p.glob("**/*.txt"))
    for i in ls:
        with i.open() as f:
            name = f.readline()[:-1]
            melody = f.readline()[:-1]
            lyrics = []
            for j in f:
                lyrics.append(j[:-1])
            songs.append({"name":name, "melody":melody, "lyrics":lyrics})

    songs.sort(key=lambda x:name)

    t = Template(template_text)
    with open("index.html", "w") as f:
        f.write(t.render(songs=songs))
    print("index.html generated")
