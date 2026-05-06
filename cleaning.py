import pandas as pd

def parse_tanggal(x):
    if pd.isna(x):
        return pd.NaT

    x = str(x).strip()

    formats = [
        "%d/%m/%Y",
        "%d/%m/%y",
        "%d %b %Y",
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%d-%m-%Y"
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except:
            continue

    return pd.NaT


def clean_data(file):
    # load data
    df = pd.read_csv(file)

    # hapus duplikat
    df = df.drop_duplicates()

    # pastikan kolom ada
    df.columns = df.columns.str.strip()

    # handle missing kota
    df["Kota"] = df["Kota"].fillna("Unknown")

    # normalisasi kota
    df["Kota"] = df["Kota"].str.title().str.strip()
    df["Kota"] = df["Kota"].replace({
        "Jkt": "Jakarta",
        "Jakrta": "Jakarta",
        "Unknown": "Unknown"
    })

    # parsing tanggal (tanpa warning)
    df["Tanggal"] = df["Tanggal"].apply(parse_tanggal)

    # convert sales ke numeric
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

    return df