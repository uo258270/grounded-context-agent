# Grounded Context Agent: Autonomous Legal Tech Agent with RAG and Self-Reflection

**Academic Context**
* **Course:** Information Retrieval
* **Instructor:** Birger Moell
* **Author:** Nuria San Emeterio Rodriguez

---

## 1. Overview & Purpose
Grounded Context Agent is an autonomous Artificial Intelligence agent designed for the Legal Tech sector. The primary purpose of this system is to act as a highly reliable Information Retrieval (IR) assistant for legal professionals. 

While standard Large Language Models (LLMs) are prone to hallucinating legal statutes, penalties, or case law, Grounded Context Agent solves this by restricting the model's knowledge exclusively to a verified local database (a Penal Code corpus). It analyzes active case files, queries the local corpus using Retrieval-Augmented Generation (RAG), and self-evaluates its conclusions before presenting them to the user.

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
    pip install openai python-dotenv

### Setup
1. Clone this repository.
2. Create a `.env` file in the root directory and add your Berget.AI API key:
    BERGET_API_KEY=your_api_key_here
3. Populate the `data/penal_code.txt` with your statutory corpus and set up the `workspace/user.md` with the active case details.

### Execution Modes

**A. Interactive Chat Mode**
Launch the conversational agent to query the legal corpus and manually instruct memory persistence.
    python3 agent.py

*Commands available in chat:*
* `remember: [fact]` -> Saves a specific conclusion to long-term memory.
* `compact` -> Forces the LLM to summarize and compress the `MEMORY.md` file to optimize the context window.
* `exit` -> Terminates the session.

**B. Autonomous Mode (The Heartbeat)**
Run the background process to observe the agent autonomously compacting memory and verifying the active case state against the law.
    python3 heartbeat.py

## 4. Interactive Examples & Evaluation (Stress Testing)
To validate the robustness of the RAG implementation and the `SupportChecker` verification module, the system was subjected to various edge cases. Below are the actual terminal outputs from the testing phase.

### Case A: Out-of-Domain Rejection
Testing if the RAG system refuses to answer questions outside its local corpus.

**User Prompt:** > "A driver was caught speeding at 120 km/h in a residential zone. What is the penalty based on the retrieved context?"

**Agent Output:**
    Agent:
    Based on the provided context, there is no information regarding speeding penalties or traffic laws. The retrieved documents cover assault, thievery, burglary, fraud, vandalism, and trespassing, but do not contain any statutes related to vehicle speed or residential zone violations.

    ---
    Support label: SUPPORTED
    Support score: 1.000
    Verification note: The Answer correctly states that there is no information regarding speeding penalties or traffic laws in the provided context, as the retrieved documents only cover specific penal codes (assault, thievery, burglary, etc.).

### Case B: Hallucination Prevention (The Trap)
Testing if the system invents unprovided details (e.g., prison sentences) for existing laws.

**User Prompt:** > "A suspect committed digital identity theft (Section 305). What is the exact prison sentence for this crime according to the penal code?"

**Agent Output:**
    Agent:
    Based on the provided penal code, Section 305 (Digital Identity Theft) is classified as a **Class 3 Felony** and carries a mandatory minimum fine of 2,000 USD. The provided text does not specify the exact prison sentence associated with a Class 3 Felony.

    ---
    Support label: SUPPORTED
    Support score: 1.000
    Verification note: The answer accurately reflects the information provided in Source: data/penal_code.txt [SECTION 305: DIGITAL IDENTITY THEFT], which states it is a Class 3 Felony with a mandatory minimum fine of 2,000 USD, and the text contains no mention of a prison sentence for this classification.

### Case C: State Management & Stale Context Overrides
Testing how the system handles a user prompt that contradicts the official active case file (`workspace/user.md`). In this test, the active case file described a window-breaking burglary, but the user asked a hypothetical question about embezzlement.

**User Prompt:** > "An employee secretly transferred 5,000 USD from the corporate bank account to their personal account. Which specific charge applies: Thievery (Section 201) or Embezzlement (Section 210)?"

**Agent Output:**
    Agent:
    Based on the provided context, the specific charge that applies is **Embezzlement (Section 210)**.

    ---
    Support label: HALLUCINATED
    Support score: 0.000
    Verification note: The Answer identifies the charge as Embezzlement (Section 210) and claims the subject is an employee transferring funds. However, the Context states the subject entered a commercial property by breaking a window and removed electronic equipment valued at 450 USD. This matches Section 205 (Burglary), not Section 210.

*Note: This strictly proves the architecture treats physical workspace documents as the ultimate source of truth over conversational prompts, effectively catching "Stale State" context errors.*

## 5. Reflection on AI and Development Challenges
Working with open-weights models like `gemma-4-31b-it` presented unique engineering challenges. During development, the model occasionally hallucinated tool executions by leaking raw internal tags (e.g., `<|tool_call>`) into plain text rather than formatting proper JSON function calls. This required implementing strict system prompting and robust parsing fallbacks in the agent loop to filter out leaked tags.

Furthermore, implementing the `SupportChecker` highlighted the critical nature of Context Engineering. Initially, the verification module returned false-positive hallucination flags because its context window only contained the retrieved laws, lacking the user's specific case facts. Aligning the context windows between the generation and verification modules was essential to achieve a reliable, grounded evaluation loop.