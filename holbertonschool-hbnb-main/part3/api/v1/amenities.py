"""Amenities API: GET public; POST and PUT admin-only."""
from flask import request
from flask_restx import Namespace, Resource, fields

from .rbac import admin_required

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Name"),
    "created_at": fields.DateTime(description="Created at"),
    "updated_at": fields.DateTime(description="Updated at"),
})

amenity_input_model = api.model("AmenityInput", {
    "name": fields.String(required=True, description="Amenity name"),
})


@api.route("/")
class AmenityList(Resource):
    @api.response(200, "List of amenities")
    def get(self):
        """List all amenities. Public."""
        from services import facade
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @admin_required
    @api.expect(amenity_input_model, validate=True)
    @api.response(201, "Amenity created", amenity_model)
    @api.response(400, "Invalid input")
    def post(self):
        """Create a new amenity. Admin only."""
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        if not name:
            return {"error": "name required"}, 400
        try:
            from services import facade
            amenity = facade.create_amenity({"name": name})
            return amenity.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details", amenity_model)
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity by ID. Public."""
        from services import facade
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @admin_required
    @api.expect(amenity_input_model)
    @api.response(200, "Amenity updated", amenity_model)
    @api.response(400, "Invalid input")
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """Update an amenity. Admin only."""
        data = request.get_json() or {}
        name = (data.get("name") or "").strip() if "name" in data else None
        payload = {} if name is None else {"name": name}
        if not payload:
            from services import facade
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": "Amenity not found"}, 404
            return amenity.to_dict(), 200
        try:
            from services import facade
            amenity = facade.update_amenity(amenity_id, payload)
            if not amenity:
                return {"error": "Amenity not found"}, 404
            return amenity.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
