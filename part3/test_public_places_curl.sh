#!/bin/bash
# Test public GET /api/v1/places endpoints without JWT (cURL).
# Run from part3 with API server on http://127.0.0.1:5000
# Usage: bash test_public_places_curl.sh

BASE="http://127.0.0.1:5000/api/v1"

echo "=============================================="
echo "1. GET /api/v1/places/ (list) - no Authorization"
echo "=============================================="
curl -s -w "\nHTTP Status: %{http_code}\n" -X GET "$BASE/places/"
echo ""

echo "=============================================="
echo "2. GET /api/v1/places/<place_id> (detail) - no Authorization"
echo "   (using first place id from list, or sample uuid if empty)"
echo "=============================================="
PLACE_ID=$(curl -s "$BASE/places/" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['id'] if isinstance(d,list) and d else '00000000-0000-0000-0000-000000000001')" 2>/dev/null || echo "00000000-0000-0000-0000-000000000001")
curl -s -w "\nHTTP Status: %{http_code}\n" -X GET "$BASE/places/$PLACE_ID"
echo ""

echo "=============================================="
echo "Done. Expected: list 200 + JSON array; detail 200 (found) or 404 (not found)."
echo "=============================================="
