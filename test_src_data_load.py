import io
import codecs
import csv

# Mirrors plugins/conditions/mm/load_data.py (BOM_CHAR, SNIFFER_SAMPLE_SIZE,
# CologneLoader.COLUMN_MAP). Importing that module directly requires the full
# Django/opal app environment, which isn't set up for this standalone script,
# so the constants are duplicated here. Keep in sync with load_data.py.
BOM_CHAR = codecs.BOM_UTF8.decode("utf-8")
SNIFFER_SAMPLE_SIZE = 16384
COLUMN_MAP = {
    "status zuletzt": "status bei letztem kontakt",
    "molekular-zytogenetik durchgeführt": "zytogenetik ja/nein",
    "high risk? 17p ,(1q21 zugewinn) bei r-iss nicht dabei, 4;14, 14;16": "hochrisiko zytogen. (a) del17p, b) t(4;14), 3) t(14;16)",
    "ldh u/i": "ldh u/l (norm bis 250)",
    "ß2m mg/l": "ß2m mg/l (<3,5 oder >5,5mg/l)",
    "albumin g/dl": "albumin g/l (>35g/dl = normal)",
    "r-iss ed": "r-iss bei ed",
    "iss ed": "iss mm ed",

    # Treatment Line mappings
    "datum ende 1. linie": "datum ende 1.-linie",
    "welche 1. linie": "art der 1st-line",

    "warum keine 2. therapie": "keine therapie 2. linie grund",
    "welche 2. linie": "art 2. linie2",

    "wenn keine indikation für 3.-linie: warum?": "keine therapie 3. line grund2",
    "warum keine 3. therapie": "keine therapie 3. line grund2",
    "datum beginn 3. linie": "datum beginn 3. linie2",
    "datum ende 3. linie": "datum ende 3. linie",
    "welche 3. linie": "art 3. linie",

    "keine therapie 4. line grund?": "keine therapie 4. line grund2",
    "welche 4. linie": "art der 4.linie",

    "keine 5. linie  grund": "keine 5. linie grund",
    "warum keine 5. linie": "keine 5. linie grund",
    "welche 5. linie": "art der 5. linie",

    "welche 6. linie": "art der 6. linie",
}


def load_rows(data):
    pos = data.tell()
    # Read a sample rather than a single line: a quoted header field can
    # contain an embedded line break, which would otherwise truncate the
    # sample mid-quote and cause the sniffer to misdetect the delimiter.
    sample = data.read(SNIFFER_SAMPLE_SIZE)
    if not sample:
        print("Empty header line!")
        return
    dialect = csv.Sniffer().sniff(sample)
    data.seek(pos)
    rows = list(csv.DictReader(
        data,
        dialect=dialect,
        quotechar='"',
        doublequote=True,
        skipinitialspace=True
    ))

    normalized_rows = []
    for _row in rows:
        # Clean keys (lowercase, strip, drop any leading UTF-8 BOM, and
        # collapse whitespace) so header cells whose quoted text wraps
        # onto multiple physical lines still match COLUMN_MAP entries.
        raw_row = {
            " ".join(k.strip().lower().lstrip(BOM_CHAR).split()): v
            for k, v in _row.items() if k is not None
        }
        # Normalize the row: Use the mapped name if it exists, else keep original
        normalized_row = {
            COLUMN_MAP.get(key, key): value
            for key, value in raw_row.items()
        }
        normalized_rows.append(normalized_row)

    row0_dict = normalized_rows[0]
    print(f"{len(row0_dict.keys())} columns loaded")
    print(f"Columns: {row0_dict.keys()}")
    print(len(normalized_rows), "rows loaded")



def test():
    # 1. Define the filename
    src_filename = "OncoCologne_202607.csv"

    # 3. Open the file in binary mode for reading
    with open(f"./dummydata/{src_filename}", 'rb') as f:
        # Decode the binary content to a string
        content = f.read().decode("utf-8")
        load_rows(io.StringIO(content))


if __name__ == "__main__":
    test()