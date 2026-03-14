"""Training tools — VO2 Max, readiness, HRV, performance metrics."""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_vo2max(date: str) -> dict:
    """Get VO2 Max estimate for running and cycling fitness level.

    Use this when the user asks about their aerobic capacity, VO2 max,
    cardiorespiratory fitness, or wants to track fitness improvements.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_vo2max(date)


@mcp.tool()
async def get_training_readiness(date: str) -> dict:
    """Get Training Readiness score indicating how prepared the body is for training.

    Use this when the user asks if they should train today, their readiness score,
    recovery status, or whether they are ready for a hard workout.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_training_readiness(date)


@mcp.tool()
async def get_training_status(date: str) -> dict:
    """Get training status showing current fitness trend and training load.

    Use this when the user asks about their training status, whether they are
    overreaching, peaking, maintaining, or detraining.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_training_status(date)


@mcp.tool()
async def get_hrv(date: str) -> dict:
    """Get Heart Rate Variability (HRV) data and overnight HRV status.

    Use this when the user asks about HRV, heart rate variability, autonomic
    nervous system balance, or recovery quality based on HRV.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_hrv(date)


@mcp.tool()
async def get_endurance_score(start_date: str, end_date: str) -> dict:
    """Get endurance fitness score over a date range.

    Use this when the user asks about their endurance fitness, aerobic base,
    or endurance capacity over a period of time.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_endurance_score(start_date, end_date)


@mcp.tool()
async def get_hill_score(start_date: str, end_date: str) -> dict:
    """Get hill climbing performance score over a date range.

    Use this when the user asks about their climbing ability, hill performance,
    or uphill fitness score.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_hill_score(start_date, end_date)


@mcp.tool()
async def get_race_predictions() -> dict:
    """Get predicted race finish times for 5K, 10K, half marathon, and full marathon.

    Use this when the user asks about their predicted race times, expected finish
    times, or race performance estimates based on current fitness.
    """
    client = await get_client()
    return await client.get_race_predictions()


@mcp.tool()
async def get_fitness_age(date: str) -> dict:
    """Get estimated fitness age based on current fitness level.

    Use this when the user asks about their fitness age, biological fitness,
    or how their fitness compares to their chronological age.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_fitness_age(date)


@mcp.tool()
async def get_personal_records() -> dict:
    """Get all personal records across activities.

    Use this when the user asks about their PRs, personal bests, fastest times,
    longest distances, or record performances.
    """
    client = await get_client()
    return await client.get_personal_records()


@mcp.tool()
async def get_lactate_threshold() -> dict:
    """Get lactate threshold heart rate and pace.

    Use this when the user asks about their lactate threshold, anaerobic threshold,
    threshold pace, or the heart rate at which they begin accumulating lactate.
    """
    client = await get_client()
    return await client.get_lactate_threshold()


@mcp.tool()
async def get_cycling_ftp() -> dict:
    """Get Functional Threshold Power (FTP) for cycling.

    Use this when the user asks about their cycling FTP, power threshold,
    watt output capacity, or cycling fitness measured in power.
    """
    client = await get_client()
    return await client.get_cycling_ftp()
