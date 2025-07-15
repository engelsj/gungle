#!/usr/bin/env python3

import subprocess
import sys


def main() -> None:
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "src.gungle.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("Development server stopped")
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
