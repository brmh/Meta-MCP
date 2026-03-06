import pytest
from unittest.mock import AsyncMock, patch
from api.client import MetaAPIClient

@pytest.fixture
def mock_meta_client():
    mock_instance = AsyncMock()
    mock_instance.get = AsyncMock(return_value={"data": [], "paging": {}})
    mock_instance.post = AsyncMock(return_value={"id": "123456789", "success": True})
    mock_instance.delete = AsyncMock(return_value={"success": True})
    
    with patch.object(MetaAPIClient, "initialize", new_callable=AsyncMock) as mock_init:
        mock_init.return_value = mock_instance
        yield mock_instance
