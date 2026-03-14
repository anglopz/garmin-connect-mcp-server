"""Tests for Garmin MCP prompts."""

import pytest
from mcp.server.fastmcp.prompts import base


def _msg_text(message: base.Message) -> str:
    """Extract text from a message, handling both str and TextContent."""
    content = message.content
    if isinstance(content, str):
        return content
    return content.text


@pytest.mark.asyncio
async def test_analyze_recent_training_default():
    from garmin_mcp.prompts.training_analysis import analyze_recent_training

    messages = await analyze_recent_training()
    assert len(messages) == 1
    assert isinstance(messages[0], base.UserMessage)
    assert "7 days" in _msg_text(messages[0])


@pytest.mark.asyncio
async def test_analyze_recent_training_custom_days():
    from garmin_mcp.prompts.training_analysis import analyze_recent_training

    messages = await analyze_recent_training(days=14)
    assert len(messages) == 1
    assert "14 days" in _msg_text(messages[0])


@pytest.mark.asyncio
async def test_sleep_quality_report_default():
    from garmin_mcp.prompts.sleep_report import sleep_quality_report

    messages = await sleep_quality_report()
    assert len(messages) == 1
    assert isinstance(messages[0], base.UserMessage)
    assert "7 days" in _msg_text(messages[0])


@pytest.mark.asyncio
async def test_sleep_quality_report_custom_days():
    from garmin_mcp.prompts.sleep_report import sleep_quality_report

    messages = await sleep_quality_report(days=30)
    assert len(messages) == 1
    assert "30 days" in _msg_text(messages[0])


@pytest.mark.asyncio
async def test_training_readiness_check():
    from garmin_mcp.prompts.readiness_check import training_readiness_check

    messages = await training_readiness_check()
    assert len(messages) == 1
    assert isinstance(messages[0], base.UserMessage)
    assert "readiness" in _msg_text(messages[0]).lower()


@pytest.mark.asyncio
async def test_health_summary():
    from garmin_mcp.prompts.health_summary import health_summary

    messages = await health_summary()
    assert len(messages) == 1
    assert isinstance(messages[0], base.UserMessage)
    assert "health" in _msg_text(messages[0]).lower()
