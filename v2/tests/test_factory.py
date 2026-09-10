from mylife.factory import create_repository
from mylife.repository import MemoryDiaryRepository


def test_no_cloud_project_uses_memory_repository():
    assert isinstance(create_repository(None), MemoryDiaryRepository)
