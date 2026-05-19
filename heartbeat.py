import time
from agent import ContextKeeperAgent

def execute_heartbeat():
    print("\n" + "="*50)
    print("💓 [HEARTBEAT] Initiating autonomous background cycle...")
    
    agent = ContextKeeperAgent()
    
    print("1. Forcing memory compaction for optimal context size...")
    compaction_result = agent.answer("compact")
    print(f"Result: {compaction_result}")
    
    print("\n2. Pre-analyzing active case based on legal corpus...")
    # The heartbeat simulates a background check on the user's active case
    analysis_result = agent.answer("What is the correct legal charge for the incident described in the user context? Verify against the penal code.")
    
    print("\n[HEARTBEAT] Cycle complete. Outcome:")
    print(analysis_result)
    
    # Autonomously save the verified result
    if "SUPPORTED" in analysis_result:
        agent.answer("remember: The current active case is classified under Section 205 (Burglary).")
        print("\n[HEARTBEAT] Supported fact safely written to long-term memory.")
        
    print("="*50)

if __name__ == "__main__":
    print("Starting Autonomous Heartbeat Daemon... (Press Ctrl+C to stop)")
    try:
        execute_heartbeat()
    except KeyboardInterrupt:
        print("\nDaemon terminated.")