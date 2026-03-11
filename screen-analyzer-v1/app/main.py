from __future__ import annotations

from app.coordinator import Coordinator
from app.ui.dashboard import Dashboard


def main():

    dashboard = Dashboard()

    coordinator = Coordinator(
        dashboard=dashboard,
        camera_source=0,
        capture_interval=3,
    )

    coordinator.start()

    dashboard.run()


if __name__ == "__main__":
    main()
