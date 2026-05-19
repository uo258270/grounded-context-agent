# Grounded Context Agent: Autonomous Legal Tech Agent with RAG and Self-Reflection

**Academic Context**
* **Course:** Information Retrieval
* **Instructor:** Birger Moell
* **Author:** Nuria San Emeterio Rodriguez

---

## 1. Overview & Purpose
Grounded Context Agent is an autonomous Artificial Intelligence agent designed for the Legal Tech sector. The primary purpose of this system is to act as a highly reliable Information Retrieval (IR) assistant for legal professionals.

## 1. Overview & Purpose
ContextKeeper is an autonomous Artificial Intelligence agent designed for the Legal Tech sector. The primary purpose of this system is to act as a highly reliable Information Retrieval (IR) assistant for legal professionals. 

While standard Large Language Models (LLMs) are prone to hallucinating legal statutes, penalties, or case law, ContextKeeper solves this by restricting the model's knowledge exclusively to a verified local database (a Penal Code corpus). It analyzes active case files, queries the local corpus using Retrieval-Augmented Generation (RAG), and self-evaluates its conclusions before presenting them to the user.

## 2. System Architecture
The project is built using object-oriented principles, separating concerns into specific modules to ensure scalability when interfacing with the Berget.AI API (using the `google/gemma-4-31b-it` model). The architecture is heavily inspired by the OpenClaw framework.

* **`llm_client.py`**: Handles secure API communication.
* **`tools/retrieval.py`**: The RAG module. Scans local `.txt` files in the `data/` directory to inject relevant statutory clauses.
* **`tools/memory.py`**: Manages long-term state via `workspace/MEMORY.md`, allowing the agent to persist verified facts.
* **`agent.py`**: The core orchestration loop handling context assembly, tool execution, and memory compaction.
* **`heartbeat.py`**: An autonomous daemon simulating a background cronjob. It wakes the agent to perform memory compaction and pre-analyze cases without human intervention.
* **`verification/support_checker.py`**: The Anti-Hallucination module utilizing an "LLM-as-a-Judge" pattern.

## 3. Installation and Usage

### Prerequisites
Ensure you have Python 3 installed. Install the required dependencies:
`pip install openai python-dotenv`

### Setup
1. Clone this repository.
2. Create a `.env` file in the root directory and add your Berget.AI API key:
   `BERGET_API_KEY=your_api_key_here`
3. Populate the `data/penal_code.txt` with your statutory corpus and set up the `workspace/user.md` with the active case details.

### Execution Modes

**A. Interactive Chat Mode**
Launch the conversational agent to query the legal corpus and manually instruct memory persistence.
`python3 agent.py`

*Commands available in chat:*
* `remember: [fact]` -> Saves a specific conclusion to long-term memory.
* `compact` -> Forces the LLM to summarize and compress the `MEMORY.md` file to optimize the context window.
* `exit` -> Terminates the session.

**B. Autonomous Mode (The Heartbeat)**
Run the background process to observe the agent autonomously compacting memory and verifying the active case state against the law.
`python3 heartbeat.py`

## 4. Interactive Examples & Evaluation (Stress Testing)
To validate the robustness of the RAG implementation and the `SupportChecker` verification module, the system was subjected to various edge cases.

### Case A: Out-of-Domain Rejection
Testing if the RAG system refuses to answer questions outside its local corpus.
* **User Prompt:** "A driver was caught speeding at 120 km/h in a residential zone. What is the penalty based on the retrieved context?"
* **Agent Behavior:** The retrieval tool returns no matching documents. The agent safely replies: *"I do not have enough retrieved context to answer this reliably."*
* **Result:** Demonstrates strict groundedness.

### Case B: Hallucination Prevention (The Trap)
Testing if the system invents unprovided details (e.g., prison sentences) for existing laws.
* **User Prompt:** "A suspect committed digital identity theft (Section 305). What is the exact prison sentence for this crime?"
* **Agent Behavior:** The agent notes that Section 305 specifies a Class 3 Felony and a fine, but explicitly states that the text *does not specify a prison sentence*.
* **SupportChecker Output:** `SUPPORTED` (Score: 1.000). The judge verifies that the model successfully avoided hallucinating standard prison terms.

### Case C: State Management & Stale Context Overrides
Testing how the system handles a user prompt that contradicts the official case file (`user.md`).
* **User Prompt:** "An employee transferred 5,000 USD from the corporate account. Is this Embezzlement?"
* **Agent Behavior:** The conversational agent reasons correctly based on the prompt. However, the `user.md` file stated the case was about breaking a window (Burglary).
* **SupportChecker Output:** `HALLUCINATED` (Score: 0.000). The judge cross-references the official `user.md` state, realizes the user's hypothetical prompt contradicts the persistent case file, and flags the response. 
* **Result:** Proves the architecture treats physical workspace documents as the ultimate source of truth over conversational prompts.

## 5. Reflection on AI and Development Challenges
Working with open-weights models like `gemma-4-31b-it` presented unique engineering challenges. During development, the model occasionally hallucinated tool executions by leaking raw internal tags (e.g., `<|tool_call>`) into plain text rather than formatting proper JSON function calls. This required implementing strict system prompting and robust parsing fallbacks in the agent loop to filter out leaked tags.

Furthermore, implementing the `SupportChecker` highlighted the critical nature of Context Engineering. Initially, the verification module returned false-positive hallucination flags because its context window only contained the retrieved laws, lacking the user's specific case facts. Aligning the context windows between the generation and verification modules was essential to achieve a reliable, grounded evaluation loop.