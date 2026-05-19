from pathlib import Path
from llm_client import LLMClient
from tools.retrieval import DocumentRetriever
from tools.memory import Memory
from verification.support_checker import SupportChecker

class ContextKeeperAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.retriever = DocumentRetriever()
        self.memory = Memory()
        self.support_checker = SupportChecker()
        self.soul = self._load_file("workspace/soul.md")
        self.user_context = self._load_file("workspace/user.md")

    def _load_file(self, path):
        file_path = Path(path)
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return ""

    def answer(self, user_input):
        user_input = user_input.strip()

        # 1. Action: Save Memory
        if user_input.lower().startswith("remember:"):
            memory_text = user_input.replace("remember:", "", 1).strip()
            self.memory.save(memory_text)
            return "I saved this in long-term memory."

        # 2. Action: Compact Memory
        if user_input.lower().startswith("compact"):
            return self.compact_memory()

        # 3. Retrieve Context
        retrieved_docs = self.retriever.search(user_input)
        retrieved_memory = self.memory.search(user_input)

        context_parts = []
        retrieved_context_parts = []

        if self.soul:
            context_parts.append("Agent soul:\n" + self.soul)
        if self.user_context:
            context_parts.append("User/project context:\n" + self.user_context)
            retrieved_context_parts.append("User/project context:\n" + self.user_context)

        if retrieved_docs:
            context_parts.append("Retrieved documents:")
            retrieved_context_parts.append("Retrieved documents:")
            for result in retrieved_docs:
                document_text = f"Source: {result['path']}\nContent: {result['content']}"
                context_parts.append(document_text)
                retrieved_context_parts.append(document_text)

        if retrieved_memory:
            context_parts.append("Relevant memory:")
            context_parts.append(retrieved_memory)
            retrieved_context_parts.append("Relevant memory:")
            retrieved_context_parts.append(retrieved_memory)

        context = "\n\n".join(context_parts)
        retrieved_context = "\n\n".join(retrieved_context_parts)

        # 4. Context Sufficiency Check
        has_retrieved_context = bool(retrieved_docs or retrieved_memory)
        if not has_retrieved_context:
            return "I do not have enough retrieved context to answer this reliably. Please add relevant documents."

        # 5. Generate Answer
        messages = [
            {
                "role": "system",
                "content": (
                    "You are ContextKeeper, an Information Retrieval focused Legal AI agent. "
                    "Use the provided context to answer. "
                    "Do not invent information that is not supported by the retrieved context. "
                )
            },
            {
                "role": "user",
                "content": f"User question:\n{user_input}\n\nAvailable context:\n{context}\n\nAnswer:"
            }
        ]

        answer = self.llm.chat(messages)

        # 6. Verification Step (Self-Correction/Groundedness)
        verification = self.support_checker.verify(
            answer=answer,
            retrieved_context=retrieved_context
        )

        return (
            f"{answer}\n\n"
            f"---\n"
            f"✅ Support label: {verification.label}\n"
            f"📊 Support score: {verification.score:.3f}\n"
            f"📝 Verification note: {verification.explanation}"
        )
    
    def compact_memory(self):
        memory_text = self.memory.read()
        if not memory_text.strip() or memory_text.strip() == "# Long-term Memory":
            return "There is no memory to compact."

        messages = [
            {
                "role": "system",
                "content": "Summarize the provided memory into a concise bulleted list of stable facts."
            },
            {
                "role": "user",
                "content": f"Current memory:\n{memory_text}\n\nCreate a compact long-term memory summary:"
            }
        ]

        compacted = self.llm.chat(messages)
        compacted_text = "# Long-term Memory\n\n" + compacted.strip() + "\n"
        Path("workspace/MEMORY.md").write_text(compacted_text, encoding="utf-8")
        return "Memory was compacted and saved to workspace/MEMORY.md."

if __name__ == "__main__":
    agent = ContextKeeperAgent()
    print("="*60)
    print(" ⚖️  ContextKeeper Legal Agent Online.")
    print(" Commands: 'remember: [text]', 'compact', or just ask a question.")
    print(" Type 'exit' to quit.")
    print("="*60)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response = agent.answer(user_input)
        print(f"\n🤖 Agent:\n{response}")