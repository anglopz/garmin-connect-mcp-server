"""Training readiness check prompt."""

from mcp.server.fastmcp.prompts import base

from garmin_mcp.server import mcp


@mcp.prompt()
async def training_readiness_check() -> list[base.Message]:
    """Check current training readiness and recommend today's workout intensity.

    Use this prompt to assess whether today is a good day for hard training,
    easy recovery, or rest based on current readiness metrics.
    """
    return [
        base.UserMessage(
            content=(
                "Please check my current training readiness using my Garmin data. "
                "Fetch my training readiness score, body battery level, HRV status, "
                "and recent sleep quality. Based on these metrics, tell me: "
                "my overall readiness score and what it means, "
                "whether today is suitable for hard training, easy effort, or rest, "
                "which specific metrics are dragging down readiness (if any), "
                "and a concrete recommendation for today's workout type and intensity."
            )
        )
    ]
