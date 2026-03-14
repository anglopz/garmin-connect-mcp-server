"""Daily health summary prompt."""

from mcp.server.fastmcp.prompts import base

from garmin_mcp.server import mcp


@mcp.prompt()
async def health_summary() -> list[base.Message]:
    """Summarize today's overall health metrics from Garmin data.

    Use this prompt to get a quick daily health snapshot including steps,
    heart rate, stress, sleep from last night, and body battery.
    """
    return [
        base.UserMessage(
            content=(
                "Please summarize my health metrics for today using my Garmin data. "
                "Fetch today's daily summary, heart rate data, stress levels, "
                "last night's sleep, and current body battery. "
                "Provide a concise overview of: step count and activity vs daily goal, "
                "resting heart rate and any notable spikes, "
                "stress levels throughout the day, "
                "last night's sleep quality and duration, "
                "and current body battery with charge/drain events. "
                "Highlight anything that stands out as noteworthy."
            )
        )
    ]
