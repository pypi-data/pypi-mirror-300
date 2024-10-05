import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()
load_dotenv()


def llamaparse_file_to_md(
    file_path: str, additional_parsing_instructions: str = "", by_page=False
):
    """Uses LlamaParse to parse a doc saved locally into a markdown string."""
    llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    parser = LlamaParse(
        api_key=llamaparse_api_key,
        parsing_instruction=additional_parsing_instructions,
        result_type="markdown",  # "markdown" and "text" are available
    )
    # filetype = file_path.split(".")[-1]
    # file_extractor = {f".{filetype}": parser}
    documents = parser.load_data(file_path)

    if by_page:
        parsed_md_document = [
            {"text": document.text, "page_no": i + 1}
            for i, document in enumerate(documents)
        ]
    else:
        parsed_md_document = "".join([document.text for document in documents])
    return parsed_md_document
