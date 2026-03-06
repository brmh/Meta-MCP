from typing import Optional, Literal, List, Annotated, Dict, Any
from pydantic import Field
from api.client import MetaAPIClient

async def get_ad_account(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    fields: Annotated[List[str], Field(description="Fields to return.")] = ["id", "name", "account_status", "amount_spent", "balance", "currency"]
) -> dict:
    """Gets details of an Ad Account."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}", params={"fields": fields})

async def list_ad_accounts(user_access_token: Annotated[Optional[str], Field(description="User token (defaults to system token if not provided).")] = None) -> dict:
    """Lists ad accounts the user has access to."""
    client = await MetaAPIClient.initialize()
    params = {"fields": "id,name,account_status"}
    if user_access_token:
         params["access_token"] = user_access_token
    return await client.get("/me/adaccounts", params=params)

async def get_account_spend(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    date_preset: Annotated[str, Field(description="E.g., last_30d.")] = "last_30d"
) -> dict:
    """Quick helper to get spend for an account in a certain time period."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}/insights", params={"fields": "spend", "date_preset": date_preset})

async def get_funding_source(ad_account_id: Annotated[str, Field(description="Ad Account ID.")]) -> dict:
    """Gets funding source info for an ad account."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}", params={"fields": "funding_source,funding_source_details"})

async def get_billing_transactions(
    ad_account_id: Annotated[str, Field(description="Ad Account ID.")], 
    limit: Annotated[int, Field(description="Result limit.")] = 25, 
    after: Annotated[Optional[str], Field(description="Cursor string.")] = None
) -> dict:
    """Lists billing transactions/charges."""
    client = await MetaAPIClient.initialize()
    params = {"fields": "id,time,amount,status,payment_method,charge_type", "limit": limit}
    if after: params["after"] = after
    return await client.get(f"/{ad_account_id}/transactions", params=params)

async def get_invoices(ad_account_id: Annotated[str, Field(description="Ad Account ID.")]) -> dict:
    """Lists invoices for the ad account (if on monthly invoicing)."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}/invoices", params={"fields": "id,invoice_date,amount_due,status"})

async def get_invoice(invoice_id: Annotated[str, Field(description="Invoice ID.")]) -> dict:
    """Gets a specific invoice."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{invoice_id}", params={"fields": "id,invoice_date,amount_due,status,download_uri"})

async def get_account_limits(ad_account_id: Annotated[str, Field(description="Ad Account ID.")]) -> dict:
    """Gets spending limits and ad/adset limits for the account."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}", params={"fields": "spend_cap,amount_spent,ad_account_creation_request_status"})

async def get_account_quality(ad_account_id: Annotated[str, Field(description="Ad Account ID.")]) -> dict:
    """Gets quality and policy status details."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}", params={"fields": "account_status,disable_reason"})

async def set_spend_cap(ad_account_id: Annotated[str, Field(description="Ad Account ID.")], spend_cap: Annotated[int, Field(description="Spend cap in cents (0 to remove).")]) -> dict:
    """Updates the overall spend cap of the ad account."""
    client = await MetaAPIClient.initialize()
    return await client.post(f"/{ad_account_id}", data={"spend_cap": spend_cap})

async def get_payment_methods(ad_account_id: Annotated[str, Field(description="Ad Account ID.")]) -> dict:
    """Gets payment methods available to the account."""
    client = await MetaAPIClient.initialize()
    return await client.get(f"/{ad_account_id}/payment_methods")
