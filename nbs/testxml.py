# /// script
# dependencies = [
#     "cite-exchange==0.2.0",
#     "marimo",
#     "pydantic==2.12.5",
#     "requests==2.32.5",
#     "urn-citation==0.7.2",
# ]
# requires-python = ">=3.14"
# ///

import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(bookchoice, chapterchoice, mo, passagechoice):
    mo.md(f"*Book* {bookchoice} *Chapter* {chapterchoice} *passage* {passagechoice}")
    return


@app.cell
def _(currentpassage, mo):
    showme = None
    if currentpassage:
        showme = mo.md("\n\n".join([psg.text for psg in currentpassage]))
    showme    

    return


@app.cell
def _(corp, currentu):
    currentpassage = None
    if currentu:
        currentpassage = corp.retrieve(currentu)

    return (currentpassage,)


@app.cell
def _(bookchoice):
    bookchoice.value
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Work
    """)
    return


@app.cell
def _():
    import citable_corpus as cc

    return (cc,)


@app.cell
def _(Path):
    f = Path.cwd() / "tests" / "data" / "septuagint_latin_genesis.xml"
    return (f,)


@app.cell
def _(f):
    with open(f, 'r', encoding='utf-8') as xmlfile:
        src  = xmlfile.read()
    return (src,)


@app.cell
def _(baseurn, uc):
    urnroot = uc.CtsUrn.from_string(baseurn)
    return (urnroot,)


@app.cell
def _(passagechoice, urnroot):
    currentu = None
    if passagechoice.value:
        currentu = urnroot.set_passage(passagechoice.value)
    return (currentu,)


@app.cell
def _(urnroot):
    urnroot
    return


@app.cell
def _():
    baseurn = "urn:cts:compnov:bible.genesis.sept_latin:"
    return (baseurn,)


@app.cell
def _(baseurn, cc, src):
    corp = cc.TEIDivAbReader(src, baseurn).corpus()
    return (corp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Navigate by reference
    """)
    return


@app.cell
def _():
    import urn_citation as uc

    return (uc,)


@app.cell
def _(uc):
    uc.CtsUrn
    return


@app.cell
def _():
    import re

    return


@app.cell
def _(mo):
    bookchoice = mo.ui.dropdown(options={'Genesis':'genesis'},value='Genesis')
    return (bookchoice,)


@app.cell
def _(chapters, mo):
    chapterchoice = mo.ui.dropdown(chapters)
    return (chapterchoice,)


@app.cell
def _(mo, passages):
    passagechoice = mo.ui.dropdown(passages)
    return (passagechoice,)


@app.cell
def _(corp):
    reff = [psg.urn.passage for psg in corp.passages]
    return (reff,)


@app.cell
def _(reff):
    chapter_reff = [ref.split(".")[0] for ref in reff]
    return (chapter_reff,)


@app.cell
def _(chapter_reff):
    chapters = list(dict.fromkeys(chapter_reff))
    return (chapters,)


@app.cell
def _(chapterchoice, reff):
    passages = []
    if chapterchoice.value:
        passages = [psg for psg in reff if psg.startswith(chapterchoice.value + ".") ]
    return (passages,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Learn xml parsing
    """)
    return


@app.cell
def _():
    import xml.etree.ElementTree as ET

    return (ET,)


@app.cell
def _():
    # 1. Define the namespace map
    nsdict = {'tei': 'http://www.tei-c.org/ns/1.0'}
    return (nsdict,)


@app.cell
def _(ET, f):
    tree = ET.parse(str(f))
    root = tree.getroot()
    return root, tree


@app.cell
def _(nsdict, root):
    divlist = [div for div in root.findall('./tei:text/tei:body/tei:div', nsdict)]
    return (divlist,)


@app.cell
def _(nsdict, tree):
    aball = [div for div in tree.findall('./tei:text/tei:body/tei:div/tei:ab', nsdict)]
    return (aball,)


@app.cell
def _(divlist, mo):
    mo.md(f"""
    FOUND **{len(divlist)}** citable divs!
    """)
    return


@app.cell
def _(aball, mo):
    mo.md(f"""
    FOUND **{len(aball)}** citable abs
    """)
    return


@app.cell
def _(divlist):
    divlist[0].tag
    return


@app.cell
def _(divlist):
    divlist[1].text
    return


@app.cell
def _(ET, baseurn, divlist, nsdict):
    flatlines = []
    for d in divlist:
        u1 = baseurn + d.get('n')
        sub_abs = d.findall('./tei:ab', nsdict)
        #flatlines.append(f"Found {len(sub_abs)} ab childredn of div {d.get('n')}")
        for ab in d.findall('./tei:ab', nsdict):
            u = u1 + "." + ab.get('n')
            line = u + "|" + ET.tostring(ab, encoding='unicode')
            flatlines.append(line)
    return (flatlines,)


@app.cell
def _(flatlines):
    flatlines
    return


@app.cell
def _(divlist):
    [div.get('n') for div in divlist]
    return


@app.cell
def _(divlist):
    divlist
    return


@app.cell
def _():
    import sys
    from pathlib import Path
    # Ensure local package import without requiring installation.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    return (Path,)


if __name__ == "__main__":
    app.run()
