from pathlib import Path

class DocumentRetriever:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

    def search(self, query):
        """Simple RAG implementation: Keyword matching across all .txt files."""
        results = []
        keywords = query.lower().split()
        
        for file_path in self.data_dir.glob("*.txt"):
            content = file_path.read_text(encoding="utf-8")
            paragraphs = content.split("\n\n")
            
            for para in paragraphs:
                if any(kw in para.lower() for kw in keywords):
                    results.append({
                        "path": str(file_path),
                        "score": 1.0, 
                        "content": para.strip()
                    })
        return results