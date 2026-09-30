import os

import requests
import streamlit as st

from dotenv import load_dotenv

from utils.document_export import (
    format_docx,
    format_pdf,
    format_txt
)

from utils.text_utils import (
    html_preview
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


st.markdown(
    """
    <style>

    .main-title {

        text-align: center;

        font-size: 2.5rem;

        font-weight: 700;

        margin-bottom: 0.2rem;
    }


    .subtitle {

        text-align: center;

        color: #777;

        margin-bottom: 1.5rem;
    }


    .notice {

        padding: 0.8rem 1rem;

        border-radius: 0.5rem;

        background: #fff4d6;

        border: 1px solid #ead08a;

        margin-bottom: 1rem;
    }


    .preview {

        padding: 1.2rem;

        border-radius: 0.7rem;

        background: #171717;

        color: #f5f5f5;

        max-height: 620px;

        overflow-y: auto;

        line-height: 1.6;
    }


    .preview h3 {

        color: #ffffff;

        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">'
    '⚖️ LegalEase'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Draft Generator'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="notice">'
    '<b>Important:</b> LegalEase creates draft documents '
    'for informational use. Review the result with a '
    'qualified legal professional before use.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header(
        "Settings"
    )

    st.caption(
        f"Backend: {BACKEND_URL}"
    )


    try:

        health_response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=3
        )


        if health_response.ok:

            st.success(
                "Backend connected"
            )

        else:

            st.warning(
                "Backend responded with an error"
            )


    except requests.RequestException:

        st.error(
            "Backend not reachable"
        )


# -----------------------------
# INPUT FORM
# -----------------------------

document_type = st.text_input(

    "Document Type",

    placeholder=(
        "Example: Freelance Work Contract"
    )
)


parties = st.text_area(

    "Parties Involved",

    placeholder=(
        "Example: Jane Doe (Service Provider), "
        "TechNova Inc. (Client)"
    ),

    height=110
)


terms = st.text_area(

    "Terms & Conditions",

    placeholder=(
        "Use semicolons for separate clauses: "
        "Payment within 30 days; "
        "Confidentiality must be maintained; "
        "Either party may terminate with 15 days notice"
    ),

    height=160
)


dates = st.text_input(

    "Effective Date",

    placeholder=(
        "Example: April 15, 2026"
    )
)


# -----------------------------
# SESSION STATE
# -----------------------------

if "document" not in st.session_state:

    st.session_state.document = ""


# -----------------------------
# GENERATE BUTTON
# -----------------------------

if st.button(
    "Generate Document",
    type="primary",
    use_container_width=True
):

    if not all(
        [
            document_type.strip(),
            parties.strip(),
            terms.strip(),
            dates.strip()
        ]
    ):

        st.warning(
            "Please fill in document type, "
            "parties, terms, and effective date."
        )

    else:

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms.strip(),

            "dates":
                dates.strip()
        }


        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=120
                )


                if response.ok:

                    data = (
                        response.json()
                    )

                    st.session_state.document = (
                        data["content"]
                    )

                    st.success(
                        "Document generated successfully."
                    )


                else:

                    try:

                        detail = (
                            response
                            .json()
                            .get(
                                "detail",
                                response.text
                            )
                        )

                    except Exception:

                        detail = response.text


                    st.error(
                        f"Generation failed: {detail}"
                    )


            except requests.RequestException as error:

                st.error(
                    "Could not contact the FastAPI backend. "
                    "Make sure Uvicorn is running."
                )

                st.caption(
                    str(error)
                )


# -----------------------------
# DOCUMENT PREVIEW
# -----------------------------

if st.session_state.document:

    st.divider()

    st.subheader(
        "Document Preview"
    )


    preview_column, edit_column = (
        st.columns([1.3, 1])
    )


    # Preview
    with preview_column:

        st.markdown(

            (
                '<div class="preview">'
                f'{html_preview(st.session_state.document)}'
                '</div>'
            ),

            unsafe_allow_html=True
        )


    # Editing
    with edit_column:

        st.markdown(
            "### Edit Document"
        )


        edited_document = st.text_area(

            "Editable document text",

            value=st.session_state.document,

            height=560,

            label_visibility="collapsed"
        )


        if st.button(
            "Save Edits",
            use_container_width=True
        ):

            st.session_state.document = (
                edited_document
            )

            st.success(
                "Edits saved."
            )

            st.rerun()


    # -----------------------------
    # DOWNLOAD
    # -----------------------------

    st.divider()

    st.subheader(
        "Download"
    )


    current_text = (
        st.session_state.document
    )


    document_name = "".join(

        character
        if character.isalnum()
        or character in "-_"
        else "_"

        for character
        in (
            document_type
            or "legal_document"
        ).lower()
    )


    document_name = (
        document_name.strip("_")
        or "legal_document"
    )


    txt_column, docx_column, pdf_column = (
        st.columns(3)
    )


    with txt_column:

        st.download_button(

            "Download TXT",

            data=format_txt(
                current_text
            ),

            file_name=(
                f"{document_name}.txt"
            ),

            mime="text/plain",

            use_container_width=True
        )


    with docx_column:

        st.download_button(

            "Download DOCX",

            data=format_docx(

                current_text,

                document_type
                or "Legal Document"
            ),

            file_name=(
                f"{document_name}.docx"
            ),

            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            use_container_width=True
        )


    with pdf_column:

        st.download_button(

            "Download PDF",

            data=format_pdf(

                current_text,

                document_type
                or "Legal Document"
            ),

            file_name=(
                f"{document_name}.pdf"
            ),

            mime="application/pdf",

            use_container_width=True
        )