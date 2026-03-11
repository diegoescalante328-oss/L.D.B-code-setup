from __future__ import annotations

from dotenv import load_dotenv

from app.config import load_settings
from app.coordinator import Coordinator
from app.ui.dashboard import Dashboard


def main() -> None:
    load_dotenv()
    settings = load_settings("config/settings.yaml")

    dashboard = Dashboard()
    coordinator = Coordinator(dashboard=dashboard, settings=settings)
    coordinator.start()

    try:
        dashboard.run()
    finally:
        coordinator.stop()


if __name__ == "__main__":
    main()
