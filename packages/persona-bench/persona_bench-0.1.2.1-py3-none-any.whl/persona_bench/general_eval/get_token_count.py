import argparse
import logging

_log = logging.getLogger(__name__)

try:
    from persona_bench.tooling.utils import get_token_count_over_log, test_fn

    # this will fail if tiktoken does not import
    test_fn()

except Exception:
    _log.error(
        "Could not import get_token_count_over_log from persona_bench.tooling.utils. Make sure you have tiktoken installed."
    )
    import sys

    sys.exit(1)


def setup_args():
    parser = argparse.ArgumentParser(
        description="Get the token count for a given model"
    )
    parser.add_argument("--mode", type=str, help="The text to encode")
    return parser.parse_args()


if __name__ == "__main__":
    args = setup_args()
    # load the json
    total_in = 0
    total_out = 0

    models = ["gpt-3.5", "gpt-4", "gpt-4o", "llama-370b"]
    modes = ["baseline", "cot", "demographic", "direct"]
    for model in models:
        for mode in modes:
            print(f"Model: {model}")
            print(f"Mode: {mode}")

            token_counts = get_token_count_over_log(model, mode)

            total_in += token_counts["input"]
            total_out += token_counts["output"]

            print(f"Input token count: {token_counts['input']}")
            print(f"Output token count: {token_counts['output']}")
            print(f"Score: {token_counts['score']}")
    print(f"Total input token count: {total_in}")
    print(f"Total output token count: {total_out}")
    print(f"Total token count: {total_in + total_out}")
