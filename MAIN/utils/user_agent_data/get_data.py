from user_agents import parse
from typing import Any

def get_data_by_user_agent(user_agent_str) -> list:
    user_agent = parse(user_agent_str)

    return [
        user_agent.browser.family,
        user_agent.os.family if user_agent.os.family else None,
        "mobile" if user_agent.is_mobile else "desktop" if user_agent.is_pc else None
    ]