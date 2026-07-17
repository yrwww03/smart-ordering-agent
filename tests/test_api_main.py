import asyncio
import unittest

from fastapi import FastAPI

from api import main


class ApiMainTest(unittest.TestCase):
    def test_app_exposes_health_route(self):
        self.assertIsInstance(main.app, FastAPI)
        paths = {route.path for route in main.app.routes}
        self.assertIn("/health", paths)
        self.assertEqual(asyncio.run(main.health_check()), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
