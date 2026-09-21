from __future__ import annotations

import argparse
import json

from .pipeline import run_synthetic_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Alveolar epithelial image-phenotyping pipeline")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("synthetic-demo", help="Run deterministic synthetic technical validation")
    demo.add_argument("--config", default="configs/default.yaml")
    demo.add_argument("--output", default="work/synthetic_demo")
    args = parser.parse_args()
    if args.command == "synthetic-demo":
        metrics = run_synthetic_demo(args.config, args.output)
        print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
