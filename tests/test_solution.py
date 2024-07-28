from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from src.landing.domain import LandingSolution
from src.features.landing.repositories import LandingSolutionRepository

engine = create_async_engine("sqlite://")
session = async_scoped_session(async_sessionmaker(bind=engine))


@pytest.mark.asyncio
async def test_list_active_solutions_for_carousel_returns_non_empty_list():
    # Setup
    repository = LandingSolutionRepository(session=session)
    mock_solution = LandingSolution(is_carousel_active=True, title="Test", title_carousel="Test", description="Test")
    session.execute = AsyncMock(return_value=mock_solution)

    # Execute
    result = await repository.list_active_solutions_for_carousel()

    # Verify
    assert len(result) > 0
    assert all(isinstance(solution, LandingSolution) for solution in result)


@pytest.mark.asyncio
async def test_list_active_solutions_for_carousel_returns_empty_when_no_active_solutions():
    # Setup
    repository = LandingSolutionRepository(session=session)
    session.execute = AsyncMock(return_value=[])

    # Execute
    result = await repository.list_active_solutions_for_carousel()

    # Verify
    assert len(result) == 0


@pytest.mark.asyncio
async def test_list_top_banners_returns_exactly_three_solutions():
    # Setup
    repository = LandingSolutionRepository(session=session)
    mock_solutions = [LandingSolution(is_top_active=True) for _ in range(3)]
    session.execute = AsyncMock(return_value=mock_solutions)

    # Execute
    result = await repository.list_top_banners()

    # Verify
    assert len(result) == 3
    assert all(isinstance(solution, LandingSolution) for solution in result)


@pytest.mark.asyncio
async def test_list_top_banners_returns_empty_when_no_top_active_solutions():
    # Setup
    repository = LandingSolutionRepository(session=session)
    session.execute = AsyncMock(return_value=[])

    # Execute
    result = await repository.list_top_banners()

    # Verify
    assert len(result) == 0
