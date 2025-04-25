# Capital City Time API

## Description
Query the current local time and UTC offset for a world capital city.

## Endpoint
`GET /api/time`

### Authorization
Header: `Authorization: Bearer YOUR_TOKEN`

### Parameters
| Name | Type | Description |
|------|------|-------------|
| `city` | query | Capital city (e.g., `London`, `Tokyo`) |

### Example Request

```bash
curl -X GET "http://<YOUR_IP>:5000/api/time?city=London" \
     -H "Authorization: Bearer YOUR_TOKEN"
