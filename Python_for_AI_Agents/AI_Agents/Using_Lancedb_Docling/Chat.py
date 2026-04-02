import streamlit as st
import lancedb
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()


# Initialize LanceDB connection
@st.cache_resource
def init_db():
    """Initialize database connection.

    Returns:
        LanceDB table object
    """
    db = lancedb.connect("data/lancedb")
    return db.open_table("docling")


def get_context(query: str, table, num_results: int = 5) -> str:
    """
    Search the database for relevant context.

    Args:
        query: User's question (string input from user)
        table: LanceDB table object (vector database)
        num_results: Number of results to return (default = 5)

    Returns:
        str: Concatenated context from relevant chunks with source information
    """

    # Perform semantic search in LanceDB:
    # - Converts query into an embedding vector
    # - Finds similar vectors in the table
    # - Limits results to top N (num_results)
    # - Converts output into a Pandas DataFrame for easier processing
    results = table.search(query).limit(num_results).to_pandas()

    # Initialize an empty list to store formatted context chunks
    contexts = []

    # Loop through each row (result) in the DataFrame
    for _, row in results.iterrows():
        # "_" = index (ignored)
        # "row" = actual data for one retrieved chunk

        # Extract metadata dictionary fields
        filename = row["metadata"]["filename"]  # Name of the source file
        page_numbers = row["metadata"]["page_numbers"]  # List of page numbers
        title = row["metadata"]["title"]  # Section title (if available)

        # Initialize a list to build the source citation
        source_parts = []

        # If filename exists (not None or empty), add it
        if filename:
            source_parts.append(filename)

        # If page numbers exist, format them as "p. 1, 2, 3"
        if page_numbers.any():  # Check if list is not empty
            source_parts.append(f"p. {', '.join(str(p) for p in page_numbers)}")
            # Breakdown:
            # str(p) → convert each page number to string
            # ', '.join(...) → join with commas

        # Create the source string:
        # '\n' = new line for readability
        # ' - '.join(...) joins filename and page info with a dash
        source = f"\nSource: {' - '.join(source_parts)}"

        # If title exists, append it on a new line
        if title:
            source += f"\nTitle: {title}"

        # Combine the main text chunk with its source metadata
        # row['text'] contains the actual document content
        contexts.append(f"{row['text']}{source}")

    # Join all context chunks into a single string
    # '\n\n' adds spacing between chunks for clarity
    return "\n\n".join(contexts)


def get_chat_response(messages, context: str) -> str:
    """
    Get streaming response from OpenAI API.

    Args:
        messages: Chat history (list of dictionaries with roles: user/assistant)
        context: Retrieved context from database (string)

    Returns:
        str: Model's response
    """

    # Create a system prompt that controls model behavior
    # This is CRITICAL for RAG systems
    system_prompt = f"""You are a helpful assistant that answers questions based on the provided context.
    Use only the information from the context to answer questions. If you're unsure or the context
    doesn't contain the relevant information, say so.
    
    Context:
    {context}
    """
    # f-string inserts the retrieved context directly into the prompt

    # Combine system prompt with existing chat messages
    # The system message is placed first (highest priority)
    # *messages unpacks the existing chat history
    messages_with_context = [{"role": "system", "content": system_prompt}, *messages]

    # Call OpenAI API to generate a response
    stream = client.chat.completions.create(
        model="gpt-4o-mini",  # Fast and cost-efficient model
        messages=messages_with_context,  # Includes system + chat history
        temperature=0.7,  # Controls randomness (0 = strict, 1 = creative)
        stream=True,  # Enables token-by-token streaming output
    )

    # NOTE:
    # "stream" is NOT a string — it's a generator that yields tokens progressively
    # Example:
    # "Hel" → "lo" → " world"

    response = st.write_stream(stream)
    return response


# Initialize Streamlit app
st.title("📚 Document Q&A")  # Display the main title of the app

# Initialize session state for chat history
if "messages" not in st.session_state:  # Check if chat history exists
    st.session_state.messages = []  # If not, create an empty list

# Initialize database connection (cached)
table = init_db()  # Connect to LanceDB and open table

# Display previous chat messages
for message in st.session_state.messages:
    # Create chat bubble based on role (user/assistant)
    with st.chat_message(message["role"]):
        # Render message content using Markdown
        st.markdown(message["content"])

# Chat input field (user types here)
if prompt := st.chat_input("Ask a question about the document"):
    # Display user message immediately in UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message to session state (chat history)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show status box while retrieving context
    with st.status("Searching document...", expanded=False) as status:
        # Retrieve relevant document chunks using vector search
        context = get_context(prompt, table)

        # Inject custom CSS styling for search results
        st.markdown(
            """
            <style>
            .search-result {
                margin: 10px 0;
                padding: 10px;
                border-radius: 4px;
                background-color: #f0f2f6;
            }
            .search-result summary {
                cursor: pointer;
                color: #0f52ba;
                font-weight: 500;
            }
            .search-result summary:hover {
                color: #1e90ff;
            }
            .metadata {
                font-size: 0.9em;
                color: #666;
                font-style: italic;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # Display header for retrieved results
        st.write("Found relevant sections:")

        # Loop through each retrieved chunk
        for chunk in context.split("\n\n"):
            # Split chunk into text and metadata
            parts = chunk.split("\n")

            text = parts[0]  # First line is main content

            # Extract metadata into dictionary
            metadata = {
                line.split(": ")[0]: line.split(": ")[1]
                for line in parts[1:]
                if ": " in line
            }

            # Safely get source and title
            source = metadata.get("Source", "Unknown source")
            title = metadata.get("Title", "Untitled section")

            # Render styled HTML block with collapsible details
            st.markdown(
                f"""
                <div class="search-result">
                    <details>
                        <summary>{source}</summary>
                        <div class="metadata">Section: {title}</div>
                        <div style="margin-top: 8px;">{text}</div>
                    </details>
                </div>
            """,
                unsafe_allow_html=True,
            )

    # Display assistant response
    with st.chat_message("assistant"):
        # Generate response using LLM with context
        response = get_chat_response(st.session_state.messages, context)

    # Save assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
