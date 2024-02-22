from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):

    URL = "/api/v1/rooms/amenities/"
    NAME = "Testing"
    DESC = "Description"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code is not 200.")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)

    def test_create_amenity(self):

        new_name = "NEW TEST"
        new_description = "NEW"

        response = self.client.post(
            self.URL,
            data={"name": new_name, "description": new_description},
        )
        data = response.json()
        self.assertEqual(response.status_code, 200, "Status code is not 200.")
        self.assertEqual(data["name"], new_name)
        self.assertEqual(data["description"], new_description)

        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 400, "Status code is not 400.")
        self.assertIn("name", data)


class TestAmenity(APITestCase):
    NAME = "Testing"
    DESC = "Description"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESC)

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)
