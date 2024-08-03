from pathlib import Path


def get_dag_id(name: str) -> str:
    """Generate dag id from file"""
    return str(Path(name).stem.replace("_", "-").removesuffix("-dag"))


def _get_data(execution_date, **_):
    year, month, day, hour, *_ = execution_date.timetuple()
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:02}/pageviews-{year}{month:02}{day:02}-{hour:02}0000.gz"
    )
    # output_path = "/tmp/wikipageviews.gz"
    # request.urlretrieve(url, output_path)

    return url
