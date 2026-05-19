import os

def search_legal_code(query: str) -> str:
    """
    Information Retrieval Tool (RAG).
    Scans the data/penal_code.txt file to find relevant statutory sections matching keywords.
    """
    corpus_path = os.path.join("data", "penal_code.txt")
    if not os.path.exists(corpus_path):
        return "Error: Legal corpus file not found in data/ directory."
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    paragraphs = content.split("\n\n")
    relevant_chunks = []
    keywords = query.lower().split()
    
    for para in paragraphs:
        if any(kw in para.lower() for kw in keywords):
            relevant_chunks.append(para.strip())
            
    if not relevant_chunks:
        return "No explicit statutory matching found in the local corpus."
        
    return "\n---\n".join(relevant_chunks)

def read_workspace_file(filename: str) -> str:
    """Reads a specific context file from the workspace directory."""
    filepath = os.path.join("workspace", filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"File {filename} not found."

def write_to_memory(fact: str) -> str:
    """
    Action Tool. Appends newly learned facts, verifications, 
    or self-corrections persistently to MEMORY.md.
    """
    filepath = os.path.join("workspace", "MEMORY.md")
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"\n- {fact}")
        return "Workspace long-term memory updated successfully."
    except Exception as e:
        return f"Error writing to memory: {str(e)}"