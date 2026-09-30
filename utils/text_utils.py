import html
import re


def sanitize_text(text):

    if not text:
        return ""

    replacements = {

        "\u2018": "'",

        "\u2019": "'",

        "\u201c": '"',

        "\u201d": '"',

        "\u2013": "-",

        "\u2014": "-",

        "\u2022": "-",

        "\u00a0": " "
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    text = text.replace(
        "\x00",
        ""
    )

    return text.strip()


def terms_to_list(terms):

    return [

        item.strip()
        .lstrip("-•")
        .strip()

        for item in re.split(
            r";|\n",
            terms or ""
        )

        if item.strip()
    ]


def html_preview(text):

    safe_text = html.escape(
        sanitize_text(text)
    )

    paragraphs = [

        paragraph.strip()

        for paragraph
        in safe_text.split("\n")

        if paragraph.strip()
    ]

    blocks = []

    for paragraph in paragraphs:

        is_heading = (

            len(paragraph) <= 90

            and (

                paragraph.isupper()

                or paragraph.endswith(":")

                or paragraph.lower()
                in {
                    "parties",
                    "effective date",
                    "definitions",
                    "signatures",
                    "important notice",
                    "confidentiality"
                }
            )
        )

        if is_heading:

            blocks.append(
                f"<h3>{paragraph}</h3>"
            )

        else:

            blocks.append(
                f"<p>{paragraph}</p>"
            )

    return "".join(blocks)