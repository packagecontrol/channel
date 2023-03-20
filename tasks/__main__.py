import argparse
import os
import textwrap

# tasks
import crawl


def main_parser() -> argparse.ArgumentParser:
    """
    Construct the main parser.
    """
    parser = argparse.ArgumentParser(
        description=textwrap.indent(
            textwrap.dedent(
                '''
                Crawl Package Control Channel and Repositories
                '''
            ).strip(),
            '    ',
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'task',
        type=str,
        help='Task to execute',
    )
    return parser


def main():
    parser = main_parser()
    args = parser.parse_args()

    if args.task == 'crawl':
        result = crawl.run()
        try:
            # write result to github action outputs
            with open(os.environ['GITHUB_OUTPUT'], 'a') as fp:
                print(f'updated={result}'.lower(), file=fp)
        except (KeyError, OSError):
            pass


if __name__ == '__main__':  # pragma: no cover
    main()


__all__ = [
    'main',
    'main_parser',
]
