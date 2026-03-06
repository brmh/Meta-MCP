---
title: Meta Ads MCP Server
emoji: 📣
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
app_port: 7860
tags:
  - mcp
  - meta-ads
  - facebook-ads
  - marketing-api
  - llm-tools
---

# Meta Ads MCP Server

A comprehensive Model Context Protocol (MCP) server for managing and analyzing Meta Ads (Facebook/Instagram). This server exposes over 80 natural-language tools to AI agents like Claude Desktop.

## 🚀 Quick Start

To connect your Claude Desktop to this deployed server:

1. Open your Claude Desktop configuration file:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\\Claude\\claude_desktop_config.json`
2. Add the following configuration (replace `<username>` with your HF username):

```json
{
  "mcpServers": {
    "meta-ads": {
      "type": "sse",
      "url": "https://<username>-meta-ads-mcp.hf.space/sse"
    }
  }
}
```

3. Restart Claude Desktop. You should now see the `meta-ads-mcp` tools available.

---

## ⚙️ Setup Guide (Hugging Face Spaces)

To deploy your own instance of this server:

1. Create a Meta App:
   - Go to [Meta for Developers](https://developers.facebook.com/)
   - Create an App (Type: Business or Marketing)
   - Note the **App ID** and **App Secret**.
2. Generate a Long-Lived System User Access Token:
   - Go to Business Settings -> System Users
   - Assign the user to your Ad Account and hit "Generate Token".
3. Add the Hugging Face Repository Secrets (Settings -> Settings -> Repository Secrets):
   - `META_ACCESS_TOKEN`: The token you just generated.
   - `META_APP_ID`: Your App ID.
   - `META_APP_SECRET`: Your App Secret.
   - `DEFAULT_AD_ACCOUNT`: Format `act_XXXXXXXXXXXXX`.
   - `META_BUSINESS_ID`: (Optional) For catalog/dataset creation.

---

## 🔐 Required Permissions

Your Meta Access Token MUST have the following permissions granted:
- `ads_read` (For reading campaigns/insights)
- `ads_management` (For creating/editing ads)
- `business_management` (For account lookups)
- `pages_read_engagement` (For page validations)
- `pages_manage_ads` (For creatives)
- `instagram_basic` & `instagram_content_publish` (For IG creatives)
- `catalog_management` (For product feeds)
- `read_insights` (For analytics tools)

---

## 🛠️ Tool Reference

The server exposes an exhaustive list of tools divided into modules:

- **Campaigns**: `create_campaign`, `update_campaign`, `delete_campaign`, `duplicate_campaign`...
- **Ad Sets & Targeting**: `create_adset`, `build_targeting_spec`, `search_targeting_interests`...
- **Ads**: `create_ad`, `get_ad_preview`, `duplicate_ad`...
- **Creatives**: `create_image_creative`, `create_video_creative`, `upload_image_from_file`...
- **Audiences**: `create_lookalike_audience`, `create_website_audience`, `share_audience`...
- **Insights**: `get_account_insights`, `get_campaign_insights`, `create_async_report`...
- **Pixels**: `send_conversion_event`, `get_pixel_stats`...
- **Catalogs**: `create_product_feed`, `list_products`...

*Note: For a full list of tools, request Claude to "List all available Meta Ads tools".*

---

## 💡 Example Prompts

Try these prompts in Claude Desktop once connected:

1. *"Create a Traffic campaign targeting 25-45 year olds in India interested in technology, with a ₹5,000/day budget."*
2. *"Show me the performance of all active campaigns in the last 30 days, broken down by age and gender."*
3. *"Pause all ad sets spending more than $100/day with a CTR below 0.5%."*
4. *"Create a 3% lookalike audience of my website visitors from the last 60 days, targeting the US and UK."*
5. *"Upload this product image and create a carousel ad with 5 cards linking to different product pages."*
6. *"Run an async report of all campaign performance for Q1 2025, broken down by placement and device."*
7. *"Send a server-side purchase conversion event for order ID 9821 worth $149.99."*
8. *"Build a targeting spec for men 30-55 in California interested in golf, luxury cars, and travel."*
9. *"Show me which of my creatives have the highest video completion rate this month."*
10. *"Duplicate my best-performing campaign from last quarter with a 20% higher budget."*
