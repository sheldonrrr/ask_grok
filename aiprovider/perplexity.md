# Perplexity (Sonar)

Official docs: https://docs.perplexity.ai/getting-started/overview

OpenAI-compatible Chat Completions, with extra search fields on the response.

## Config

- **API Key**: required (`Authorization: Bearer …`)
- **Base URL**: `https://api.perplexity.ai`
- **Chat**: `POST ${baseUrl}/chat/completions`

```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
```

Common fields: `model`, `messages`, `temperature`, `max_tokens`, `top_p`, `stream`.

Search-related fields (official): `search_domain_filter`, `search_recency_filter`, `return_images`, `return_related_questions`, `search_mode` (`web` or `academic`).

## Models

Typical ids: `sonar`, `sonar-pro`, `sonar-reasoning-pro`, `sonar-deep-research`. There is no stable public model-list endpoint.

## Response

- Text: `choices[0].message.content` (stream: `choices[0].delta.content`)
- Optional extras: `search_results`, `images`, `usage`
