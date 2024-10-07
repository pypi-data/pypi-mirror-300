import logging

from src.models.injury import Injury
from src.repositories.fixture_stats_repository import FixtureStatsRepository
from src.repositories.injury_repository import InjuryRepository
from src.services.fixture_service import FixtureService

LOGGER = logging.getLogger(__name__)


class InjuriesService:
    def __init__(self):
        self.injuries_repository = InjuryRepository()
        self.fixture_service = FixtureService()

    def upsert_many_injuries(self, fixture_injuries):
        self.injuries_repository.bulk_upsert_documents('injuries', fixture_injuries)
        LOGGER.info('Upserted injuries data')

    def upsert_injuries(self, fixture_injuries):
        self.injuries_repository.upsert_document('injuries', fixture_injuries)
        LOGGER.info('Upserted injuries data')

    def get_injuries(self, fixture_id: str):
        response = self.injuries_repository.get_injuries(fixture_id)

        if not response.get('data', []):
            return []

        fixture_stats = [Injury.from_dict(injury) for injury in response]
        return fixture_stats

    def get_team_injuries(self, team_id: str, league_id: str, season: str):
        fixture_ids = self.fixture_service.get_fixture_ids(team_id, league_id, season)
        team_injuries = self.injuries_repository.get_team_injuries(fixture_ids)
        team_injuries = [Injury.from_dict(injuries) for injuries in team_injuries]
        return team_injuries
