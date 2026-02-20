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


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import xml.etree.ElementTree as ET

    return (ET,)


@app.cell
def _(Path):
    f = Path.cwd() / "tests" / "data" / "septuagint_latin_genesis.xml"
    return (f,)


@app.cell
def _(root):
    root.tag
    return


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
def _(nsdict, tree):
    divlist = [div for div in tree.findall('./tei:text/tei:body/tei:div', nsdict)]
    
    return (divlist,)


@app.cell
def _(nsdict, tree):
    aball = [div for div in tree.findall('./tei:text/tei:body/tei:div/tei:ab', nsdict)]
    return (aball,)


@app.cell
def _(divlist, mo):
    mo.md(f"FOUND **{len(divlist)}** citable divs!")
    return


@app.cell
def _(aball, mo):
    mo.md(f"FOUND **{len(aball)}** citable abs")
    return


@app.cell
def _():
    baseurn = "urn:cts:compnov:bible.genesis.sept_latin:"
    return (baseurn,)


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


@app.cell
def _():
    import citable_corpus as cc

    return


if __name__ == "__main__":
    app.run()
