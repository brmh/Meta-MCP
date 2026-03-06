import pytest
import asyncio
from tools.campaigns import create_campaign, get_campaign, list_campaigns, delete_campaign, update_campaign
from api.error_handler import MetaAPIError

@pytest.mark.asyncio
async def test_create_campaign_success(mock_meta_client):
    mock_meta_client.post.return_value = {"id": "camp_123"}
    
    result = await create_campaign(
        ad_account_id="act_111",
        name="Test Camp",
        objective="OUTCOME_TRAFFIC"
    )
    
    assert result == {"id": "camp_123"}
    mock_meta_client.post.assert_called_once()
    called_url, kwargs = mock_meta_client.post.call_args
    assert called_url[0] == "/act_111/campaigns"
    assert kwargs["data"]["name"] == "Test Camp"

@pytest.mark.asyncio
async def test_get_campaign(mock_meta_client):
    mock_meta_client.get.return_value = {"id": "camp_123", "name": "Test"}
    
    result = await get_campaign("camp_123")
    assert result["name"] == "Test"
    mock_meta_client.get.assert_called_once_with("/camp_123", params={"fields": ["id", "name", "status", "objective"]})

@pytest.mark.asyncio
async def test_delete_campaign_requires_confirm(mock_meta_client):
    with pytest.raises(ValueError):
        await delete_campaign("camp_123")
        
    await delete_campaign("camp_123", confirm=True)
    mock_meta_client.delete.assert_called_once_with("/camp_123")

@pytest.mark.asyncio
async def test_update_campaign_success(mock_meta_client):
    mock_meta_client.post.return_value = {"success": True}
    await update_campaign("camp_123", status="ACTIVE")
    mock_meta_client.post.assert_called_once()
    called_url, kwargs = mock_meta_client.post.call_args
    assert called_url[0] == "/camp_123"
    assert kwargs["data"]["status"] == "ACTIVE"

@pytest.mark.asyncio
async def test_list_campaigns_pagination(mock_meta_client):
    mock_meta_client.get.return_value = {"data": [{"id": "1"}], "paging": {"cursors": {"after": "abc"}}}
    res = await list_campaigns("act_111", after="xyz")
    mock_meta_client.get.assert_called_once()
    assert mock_meta_client.get.call_args[1]["params"]["after"] == "xyz"
    assert res["data"][0]["id"] == "1"
