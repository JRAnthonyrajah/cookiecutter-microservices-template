# API Documentation: {{ cookiecutter.service_name }}

## Overview

This document describes the API contract for the `{{ cookiecutter.service_slug }}` microservice. The API follows REST conventions and returns responses in JSON format.

## Base URL

```
http://localhost:{{ cookiecutter.service_port }}/api/v1
```

## Authentication

The API supports the following authentication methods:

- **API Key** (Header): `X-API-Key: your-api-key`
- **Bearer Token** (Header): `Authorization: Bearer your-token`
- **No Authentication**: For public endpoints (e.g., health check)

## Request/Response Format

### Headers

All requests should include the following headers:

```
Content-Type: application/json
Accept: application/json
X-Request-ID: unique-request-identifier (optional)
X-Correlation-ID: correlation-identifier (optional)
```

### Request Body

Requests requiring a body must send JSON-formatted data:

```json
{
  "key": "value",
  "timestamp": "2026-04-19T10:30:00Z"
}
```

### Response Format

All responses follow a consistent envelope:

```json
{
  "success": true,
  "data": {
    "id": "resource-id",
    "name": "resource-name",
    "created_at": "2026-04-19T10:30:00Z"
  },
  "error": null,
  "metadata": {
    "request_id": "req-12345",
    "timestamp": "2026-04-19T10:30:01Z"
  }
}
```

## HTTP Status Codes

| Code | Description | Use Case |
|------|-------------|----------|
| 200 | OK | Successful GET, POST, PUT, PATCH requests |
| 201 | Created | Successful resource creation (POST) |
| 204 | No Content | Successful DELETE request with no response body |
| 400 | Bad Request | Invalid request parameters or format |
| 401 | Unauthorized | Missing or invalid authentication credentials |
| 403 | Forbidden | Authenticated but lacks permission for resource |
| 404 | Not Found | Requested resource does not exist |
| 409 | Conflict | Resource conflict (e.g., duplicate creation attempt) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Service is temporarily unavailable |

## Rate Limiting

The API implements token bucket rate limiting:

- **Default Limit**: 1,000 requests per 15 minutes per API key
- **Burst Limit**: 100 requests per minute
- **Premium Tier**: 10,000 requests per 15 minutes

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 2026-04-19T10:45:00Z
```

## Endpoints

### 1. Health Check

**GET** `/health`

Check the service health status. No authentication required.

**Request:**

```bash
curl -X GET http://localhost:{{ cookiecutter.service_port }}/api/v1/health \
  -H "Content-Type: application/json"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "{{ cookiecutter.service_slug }}",
    "version": "1.0.0",
    "uptime_seconds": 3600,
    "dependencies": {
      "database": "connected",
      "cache": "connected",
      "messaging": "healthy"
    }
  },
  "error": null,
  "metadata": {
    "request_id": "health-check-001",
    "timestamp": "2026-04-19T10:30:00Z"
  }
}
```

### 2. Get Data

**GET** `/data/{id}`

Retrieve a specific data resource by ID.

**Authentication**: Required (API Key or Bearer Token)

**Path Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `id` | string | The unique identifier of the resource |

**Query Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `include_metadata` | boolean | false | Include extended metadata |
| `format` | string | json | Response format (json, xml) |

**Request:**

```bash
curl -X GET http://localhost:{{ cookiecutter.service_port }}/api/v1/data/123 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -H "X-Request-ID: req-12345"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Sample Data",
    "description": "A sample resource",
    "status": "active",
    "created_at": "2026-04-18T10:30:00Z",
    "updated_at": "2026-04-19T10:30:00Z"
  },
  "error": null,
  "metadata": {
    "request_id": "req-12345",
    "timestamp": "2026-04-19T10:30:00Z"
  }
}
```

### 3. Create Data

**POST** `/data`

Create a new data resource.

**Authentication**: Required (API Key or Bearer Token)

**Request:**

```bash
curl -X POST http://localhost:{{ cookiecutter.service_port }}/api/v1/data \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"name": "New Resource", "description": "A new resource"}'
```

**Response (201 Created):**

```json
{
  "success": true,
  "data": {
    "id": "124",
    "name": "New Resource",
    "status": "active",
    "created_at": "2026-04-19T10:30:00Z"
  },
  "error": null,
  "metadata": {
    "request_id": "req-12346",
    "timestamp": "2026-04-19T10:30:00Z"
  }
}
```

### 4. Update Data

**PUT** `/data/{id}` - Full replacement

**PATCH** `/data/{id}` - Partial update

**Authentication**: Required (API Key or Bearer Token)

**Request:**

```bash
curl -X PATCH http://localhost:{{ cookiecutter.service_port }}/api/v1/data/123 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"name": "Updated Resource"}'
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Updated Resource",
    "status": "active",
    "updated_at": "2026-04-19T10:31:00Z"
  },
  "error": null,
  "metadata": {
    "request_id": "req-12347",
    "timestamp": "2026-04-19T10:31:00Z"
  }
}
```

### 5. Delete Data

**DELETE** `/data/{id}`

Delete a data resource.

**Authentication**: Required (API Key or Bearer Token)

**Request:**

```bash
curl -X DELETE http://localhost:{{ cookiecutter.service_port }}/api/v1/data/123 \
  -H "X-API-Key: your-api-key"
```

**Response (204 No Content):**

No response body. Status code indicates success.

### 6. List Data

**GET** `/data`

List all data resources with optional filtering and pagination.

**Authentication**: Required (API Key or Bearer Token)

**Query Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `page` | integer | 1 | Page number for pagination |
| `limit` | integer | 20 | Number of items per page (max: 100) |
| `sort` | string | -created_at | Sort field and direction |
| `filter` | string | | Filter expression |
| `search` | string | | Full-text search query |

**Request:**

```bash
curl -X GET "http://localhost:{{ cookiecutter.service_port }}/api/v1/data?page=1&limit=10&sort=-created_at" \
  -H "X-API-Key: your-api-key"
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": [
    {
      "id": "123",
      "name": "Resource 1",
      "status": "active",
      "created_at": "2026-04-18T10:30:00Z"
    }
  ],
  "error": null,
  "metadata": {
    "request_id": "req-12349",
    "timestamp": "2026-04-19T10:33:00Z",
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 150,
      "total_pages": 15
    }
  }
}
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error information.

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Request parameters are invalid |
| `UNAUTHORIZED` | 401 | Authentication is missing or invalid |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource does not exist |
| `CONFLICT` | 409 | Resource conflict (e.g., duplicate) |
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## OpenAPI/Swagger Specification

The API provides OpenAPI 3.0 specification at:

```
GET /api/v1/openapi.json
GET /api/v1/docs
GET /api/v1/docs/swagger
```

## Versioning

The API uses URL-based versioning. Current version: `v1` (e.g., `/api/v1/data`)

Breaking changes will trigger a new version. Non-breaking changes are made to the current version.

## Rate Limiting Strategy

The API implements a token bucket algorithm:

1. **Allocation**: Each API key receives tokens at a fixed rate
2. **Consumption**: Each request consumes 1-N tokens depending on endpoint
3. **Bucket Size**: Maximum tokens stored (burst capacity)
4. **Reset**: Tokens refill at the specified rate

## Pagination

List endpoints support cursor-based and offset-based pagination:

**Offset Pagination:**
```bash
GET /data?page=2&limit=20
```

**Cursor Pagination:**
```bash
GET /data?cursor=abc123&limit=20
```

## Webhooks (Optional)

If webhooks are supported, register them at:

```
POST /webhooks/subscribe
DELETE /webhooks/unsubscribe
GET /webhooks/list
```

## SDK Support

Official SDKs are available for:

- **Python**: `pip install {{ cookiecutter.service_slug }}-sdk`
- **Node.js**: `npm install @{{ cookiecutter.org }}/{{ cookiecutter.service_slug }}-sdk`
- **Go**: `go get github.com/{{ cookiecutter.org }}/{{ cookiecutter.service_slug }}-sdk`

## Support & Contact

For API support, documentation, and issues:

- **Documentation**: https://docs.example.com
- **Issues**: https://github.com/{{ cookiecutter.org }}/{{ cookiecutter.service_slug }}/issues
- **Email**: api-support@example.com
- **Slack**: #api-support channel

## Changelog

### Version 1.0.0 (2026-04-19)

- Initial release
- Health check endpoint
- CRUD operations for data resources
- Rate limiting and pagination
- Authentication via API Key and Bearer Token
- OpenAPI documentation
