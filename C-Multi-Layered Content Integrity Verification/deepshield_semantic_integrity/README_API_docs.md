
# 📌 Semantic Integrity Requests API Documentation

> 🔗 **BASE_URL:** `https://deepshield.secublox.com`  
Use this as the base URL for all API endpoints described below.
You need to pass the following for authentication: `Authorization`: `Api-Key LvZG7La7.2OQzs8zTsVSHs4sHNVPWBNQ0MaRwJBtz`
---


## 📥 1. GET `/api/requests_pending_semantic_integrity`

Retrieves a list of all semantic integrity requests. Optionally filter the results by status: `pending`, `processed`, `failed`, or `running`.

### ✅ Request

- **Method:** `GET`

### 🔍 Query Parameters (Optional)

| Parameter   | Type   | Description                                                            |
|-------------|--------|------------------------------------------------------------------------|
| `status`    | string | Filter by request status: `pending`, `processed`, `failed`, `running` |
| `page`      | int    | Page number                                                            |
| `page_size` | int    | Number of results per page                                             |

### 📘 Example Request

```http
GET /api/requests_pending_semantic_integrity?status=pending
```

### 📦 Example Response

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "current_page": 1,
  "page_size": 10,
  "results": [
    {
      "id": 6,
      "created_at": "2025-04-22T07:43:03.734221Z",
      "updated_at": "2025-04-22T07:43:03.734309Z",
      "is_soft_deleted": false,
      "image": "http://127.0.0.1:8000/media/sim_images/20250410_174748_59002_09_pU2Zpol.jpg",
      "watermark_image": "http://127.0.0.1:8000/media/sim_images/20250410_174557_59002_08_The2aBW.jpg",
      "overall_prediction": null,
      "confidence_score": null,
      "status": "pending",
      "user": 20
    },
    {
      "id": 5,
      "created_at": "2025-04-22T07:41:52.786592Z",
      "updated_at": "2025-04-22T07:41:52.786627Z",
      "is_soft_deleted": false,
      "image": "http://127.0.0.1:8000/media/sim_images/20250410_174748_59002_09_v5SLq2L.jpg",
      "watermark_image": "http://127.0.0.1:8000/media/sim_images/20250410_174557_59002_08_b9qkWZ9.jpg",
      "overall_prediction": null,
      "confidence_score": null,
      "status": "pending",
      "user": 20
    }
  ]
}
```

---

## ✅ 2. POST `/api/semantic_integrity_results/{id}`

Updates the semantic integrity result for a specific request.

### 📥 Request

- **Method:** `POST`
- **Content-Type:** `application/json`

### 🔗 URL Parameters

- `id`: The ID of the semantic integrity request to update

### 🧾 Request Body

```json
{
  "overall_prediction": true,
  "confidence_score":100
}
```
---

## ✅ 3. PATCH `/api/semantic_integrity_status/{id}`

Updates the semantic integrity status for a specific request. The status can be set to pending, processed, failed, or running.

### 📥 Request

- **Method:** `PATCH`
- **Content-Type:** `application/json`

### 🧾 Request Body

```json
{
  "status": running"
}
```

### ✅ Allowed Status Transitions

| Current Status | Allowed Next Status       |
|----------------|---------------------------|
| `pending`      | `running`                 |
| `running`      | `processed`, `failed`     |

## 📎 Notes
- Only the `status` field can be updated via `PATCH`.
- The API enforces valid transitions:
  - `pending → running`
  - `running → failed`
  - `running → processed`
