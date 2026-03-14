"""Sleep quality report prompt."""

from mcp.server.fastmcp.prompts import base

from garmin_mcp.server import mcp


@mcp.prompt()
async def sleep_quality_report(days: int = 7) -> list[base.Message]:
    """Generate a sleep quality report for the past N days.

    Use this prompt to review sleep patterns, quality trends, and how
    sleep is affecting training readiness and recovery.

    Args:
        days: Number of days to include in the report (default 7)
    """
    return [
        base.UserMessage(
            content=(
                f"Please generate a sleep quality report covering the past {days} days "
                "using my Garmin data. Fetch my sleep data for each night and body battery trends. "
                "Summarize: average sleep duration and quality scores, sleep stage breakdown "
                "(deep, REM, light, awake), consistency of sleep/wake times, "
                "correlation between sleep quality and next-day body battery, "
                "and actionable recommendations to improve sleep."
            )
        )
    ]
