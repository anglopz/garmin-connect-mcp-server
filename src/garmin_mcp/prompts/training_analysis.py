"""Training analysis prompt."""

from mcp.server.fastmcp.prompts import base

from garmin_mcp.server import mcp


@mcp.prompt()
async def analyze_recent_training(days: int = 7) -> list[base.Message]:
    """Analyze training load, intensity, and progress over the past N days.

    Use this prompt to get a comprehensive analysis of recent training,
    including volume, intensity distribution, and recovery patterns.

    Args:
        days: Number of days to analyze (default 7)
    """
    return [
        base.UserMessage(
            content=(
                f"Please analyze my Garmin training data for the past {days} days. "
                "Use the available tools to fetch my activities, training status, "
                "training readiness, and VO2 max trends. "
                "Provide insights on: training load and volume, intensity distribution "
                "(easy vs hard sessions), recovery quality, fitness progression, "
                "and recommendations for the next training block."
            )
        )
    ]
