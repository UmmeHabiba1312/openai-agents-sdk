# 1 - Agent loop

sequenceDiagram
User->>Agent: Sends prompt
Agent->>LLM: Sends system + user prompt
LLM->>Agent: Returns either:
  - Final output
  - Tool call
  - Function handoff
Agent->>Tool: Executes tool if needed
Tool->>Agent: Returns result
Agent->>LLM: Sends tool result
LLM->>Agent: Produces final output
Agent->>User: Returns response

2 = Guardrials 
input guardrials (must be on first agent)
output guardrials (must be on last agent)