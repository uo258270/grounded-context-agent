from pathlib import Path

class Memory:
    def __init__(self, memory_path="workspace/MEMORY.md"):
        self.memory_path = Path(memory_path)
        if not self.memory_path.exists():
            self.memory_path.write_text("# Long-term Memory\n\n", encoding="utf-8")

    def save(self, text):
        current = self.read()
        new_content = current + f"\n- {text}"
        self.memory_path.write_text(new_content, encoding="utf-8")

    def read(self):
        if self.memory_path.exists():
            return self.memory_path.read_text(encoding="utf-8")
        return ""

    def search(self, query):
        # In a real app, this would filter. Here we inject the full memory context.
        return self.read()