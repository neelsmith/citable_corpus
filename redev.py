import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Read Latin glosses
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Computation
    """)
    return


@app.cell
def _():
    import citable_corpus as cc

    return (cc,)


@app.cell
def _():
    from pathlib import Path

    return (Path,)


@app.cell
def _():
    from xml.dom import minidom

    return (minidom,)


@app.cell
def _(mo):
    mo.md("""
    ## Load data
    """)
    return


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
def _():
    baseurn = "urn:cts:compnov:bible.genesis.sept_latin:"
    return (baseurn,)


@app.cell
def _(baseurn, cc, src):
    rdr = cc.TEIDivAbReader(src, baseurn)
    return (rdr,)


@app.cell
def _(rdr):
    corpus = rdr.corpus()
    return (corpus,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## XML manipulation
    """)
    return


@app.cell
def _(corpus):
    sample  = corpus.passages[2].text
    return (sample,)


@app.cell
def _(minidom, sample):
    parseddoc = minidom.parseString(sample)
    return (parseddoc,)


@app.cell
def _(cc, parseddoc):
    cc.extract_text(node=parseddoc, omitlist=['expan'], cumulation=[])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
