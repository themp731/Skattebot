"""Offline contract and static-site smoke tests for the local refresh flow."""
from __future__ import annotations

import functools
import json
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.request import urlopen

from local_pipeline import SCHEMA_VERSION, export_artifacts, generate_dummy_data, write_site


class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


class LocalPipelineTests(unittest.TestCase):
    def make_demo(self, root: Path, *, seed: int = 10, teams: int = 12, week: int = 4) -> tuple[Path, Path, Path]:
        raw, outputs, public = root / "raw", root / "outputs", root / "public"
        generate_dummy_data(raw, 2026, week, teams, seed)
        export_artifacts(raw, outputs, public, 2026, "dummy", week)
        write_site(public)
        return raw, outputs, public

    def test_dummy_generation_is_deterministic_with_a_seed(self) -> None:
        with TemporaryDirectory() as temp:
            root = Path(temp)
            first, second = root / "first", root / "second"
            generate_dummy_data(first, 2026, 4, 12, 10)
            generate_dummy_data(second, 2026, 4, 12, 10)
            for name in ("matchups.csv", "team_stats.csv", "player_stats.csv"):
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())

    def test_export_creates_the_shared_canonical_contract(self) -> None:
        with TemporaryDirectory() as temp:
            _, outputs, public = self.make_demo(Path(temp))
            latest = json.loads((public / "data" / "latest.json").read_text(encoding="utf-8"))
            context = json.loads((outputs / "recaps" / "recap_context_week_4.json").read_text(encoding="utf-8"))
            self.assertEqual(latest["metadata"]["schema_version"], SCHEMA_VERSION)
            self.assertTrue(latest["metadata"]["is_sample_data"])
            self.assertEqual(len(latest["standings"]), 12)
            self.assertEqual(len(context["week_results"]), 6)
            self.assertEqual(context["standings"], latest["standings"])
            self.assertEqual(context["rankings"], latest["rankings"])


class SiteSmokeTests(unittest.TestCase):
    def serve(self, directory: Path):
        handler = functools.partial(QuietHTTPRequestHandler, directory=str(directory))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        def stop() -> None:
            server.shutdown()
            thread.join()
            server.server_close()

        self.addCleanup(stop)
        return f"http://127.0.0.1:{server.server_address[1]}"

    def test_site_serves_published_data_and_demo_markup(self) -> None:
        with TemporaryDirectory() as temp:
            root = Path(temp)
            raw, outputs, public = root / "raw", root / "outputs", root / "public"
            generate_dummy_data(raw, 2026, 2, 4, 7)
            export_artifacts(raw, outputs, public, 2026, "dummy", 2)
            write_site(public)
            address = self.serve(public)
            index = urlopen(f"{address}/index.html").read().decode("utf-8")
            payload = json.loads(urlopen(f"{address}/data/latest.json").read().decode("utf-8"))
            self.assertIn("Skattebot dashboard", index)
            self.assertIn("DEMO DATA", index)
            self.assertTrue(payload["metadata"]["is_sample_data"])
            self.assertEqual(len(payload["standings"]), 4)

    def test_site_has_a_missing_data_fallback(self) -> None:
        with TemporaryDirectory() as temp:
            public = Path(temp) / "public"
            write_site(public)
            address = self.serve(public)
            index = urlopen(f"{address}/index.html").read().decode("utf-8")
            self.assertIn("No published league data is available", index)
            with self.assertRaises(HTTPError) as response:
                urlopen(f"{address}/data/latest.json")
            self.assertEqual(response.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
