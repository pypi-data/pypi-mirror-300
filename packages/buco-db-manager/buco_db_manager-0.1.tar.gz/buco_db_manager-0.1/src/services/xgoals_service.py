from src.models.xgoals import XGoals
from src.repositories.xgoals_repository import XGoalsRepository
from src.services.fixture_service import FixtureService


class XGoalsService:
    def __init__(self, db_name):
        self.xgoals_repository = XGoalsRepository(db_name)
        self.fixture_service = FixtureService()

    def upsert_many_fixture_xg(self, xg):
        self.xgoals_repository.upsert_many_fixture_xg(xg)

    def get_xgoals(self, fixture_id: str):
        xgoals = self.xgoals_repository.get_xgoals(fixture_id)
        return xgoals

    def get_xgoals_over_season(self, team_id: str, league_id: str, season: str):
        fixture_ids = self.fixture_service.get_fixture_ids(team_id, league_id, season)
        xgoals_over_season = self.xgoals_repository.get_many_xgoals(fixture_ids)
        xgoals_over_season = [XGoals.from_dict(response['data']) for response in xgoals_over_season]

        return xgoals_over_season
