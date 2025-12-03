import sys
import os

# Add src to path if needed, though usually running as module handles this
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui import MSIFanControlApp

def main():
    app = MSIFanControlApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
