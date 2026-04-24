#!/c/Users/JANG/claude_testing/claude_agent_learning/.venv/Scripts/python
"""Claude Agent SDK command-line runner.

Sends a prompt to the Claude Agent SDK and streams back responses,
printing each message with a timestamp.
Support partial streaming

Usage:
    python main.py <prompt> [options_json]

    prompt       - The text prompt to send to the agent.
    options_json - Optional JSON string of ClaudeAgentOptions keyword arguments.

Examples:
    # Default prompt and options
    python main.py

    # Custom prompt, default options
    python main.py "Explain quantum computing"

    # Custom prompt with options
    python main.py "Explain quantum computing" '{"model":"glm-5.1","max_turns":5,"permission_mode":"bypassPermissions"}'

    # Using a different model with fewer turns
    python main.py "Summarize this article" '{"model":"claude-sonnet-4-6","max_turns":2}'
"""

import asyncio
import json
import sys
import rich
from datetime import datetime

from claude_agent_sdk import query, ClaudeAgentOptions, get_session_messages
from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    UserMessage,
    StreamEvent,
)


def display_llm_messages(session_id: str, ind: int) -> int:
    if not session_id:
        return 0
    # await asyncio.sleep(0.1)
    session_messages = get_session_messages(session_id)
    msg_length = len(session_messages)
    # print(f'msg_length = {msg_length}, index = {ind}')
    if msg_length > ind:
        for i in range(ind, msg_length):
            print(f'\nLLM Message[{i}] {datetime.now()} {"-" * 50}')
            rich.print(session_messages[i])
    return msg_length


async def main(prompt: str, options_str: str = "{}"):
    """Run a Claude Agent query and stream the response.

    Args:
        prompt: The text prompt to send to the Claude agent.
        options_str: JSON string of keyword arguments passed to
            ClaudeAgentOptions. Defaults to "{}" (empty dict).
    """
    options_dict = json.loads(options_str)
    options = ClaudeAgentOptions(**options_dict)

    print(f"Prompt: {prompt}")
    print(f"Options: {json.dumps(options_dict, indent=2)}")
    print()

    session_id = ""
    index = 0
    result_message = None
    try:
        async for message in query(prompt=prompt, options=options):
            # Retrieve session id
            if isinstance(message, SystemMessage):
                # Get the session id
                if not session_id:
                    session_id = message.data["session_id"]

            if isinstance(message, ResultMessage):
                result_message = message

            # Process StreamEvent
            # Within your 'async for message in query(...)' loop:
            if isinstance(message, StreamEvent):
                event = message.event
                event_type = event.get("type")
                # Text arrives word-by-word in 'content_block_delta'
                if event_type == "message_start":
                    print(f"\n", flush=True)
                elif event_type == "content_block_delta":
                    delta = event.get("delta", {})
                    if delta.get("type") == "text_delta":
                        # Print the word without a newline for a typing effect
                        print(delta.get("text", ""), end="", flush=True)
                elif event_type == "content_block_stop":
                    print(f"\n", flush=True)
            else:
                # Display LLM message
                index = display_llm_messages(session_id, index)

                # Print human-readable output
                print(f'\n{datetime.now()} {"=" * 50}')
                rich.print(message, flush=True)

        # Print session context before exiting
        if result_message is not None:
            print(f'\n{"=" * 50}')
            print("Session Context:")
            print(f"  Session ID:    {result_message.session_id}")
            print(f"  Num Turns:     {result_message.num_turns}")
            print(
                f"  Duration:      {result_message.duration_ms}ms (API: {result_message.duration_api_ms}ms)"
            )
            print(
                f"  Total Cost:    ${result_message.total_cost_usd}"
                if result_message.total_cost_usd is not None
                else "  Total Cost:    N/A"
            )
            print(f"  Is Error:      {result_message.is_error}")
            print(
                f"  Stop Reason:   {result_message.stop_reason}"
                if result_message.stop_reason is not None
                else "  Stop Reason:   N/A"
            )
    except Exception as e:
        print(f"An error occurrred: {e}")

        # Retrieve and print full conversation history
        # session_messages = get_session_messages(result_message.session_id)
        # print(f'\n{"=" * 50}')
        # print(f'Session Messages ({len(session_messages)} messages):')
        # for msg in session_messages:
        #    print(f'\n  [{msg.type}] uuid={msg.uuid}')
        #    rich.print(msg.message)


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Who are you?"
    options_str = sys.argv[2] if len(sys.argv) > 2 else "{}"
    asyncio.run(main(prompt, options_str))
