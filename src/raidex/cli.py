"""
cli.py: Command-line interface to raidex.
"""

import argparse
from pathlib import Path

ACTION_BUILD = 'build'
ACTION_OPEN = 'open'


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    subparsers = parser.add_subparsers(
        title='Action',
        dest='action',
        description='Which action to perform',
        )

    _add_build_action(subparsers)
    _add_open_action(subparsers)

    args = parser.parse_args()

    if args.action == ACTION_BUILD:
        from raidex.Browser import Browser
        import raimad as rai

        browser = Browser()

        for compo in rai.flatten(
                map(
                    lambda s: rai.string_import(s, multiple=True),
                    args.packages
                    )
                ):
            browser.register_compo(compo)

        browser.generate_html(args.browser_dir)

    elif args.action == ACTION_OPEN:
        import webbrowser
        # Web browser needs to know the absolute path
        index_path = args.browser_dir.resolve() / 'index.html'
        webbrowser.open(f'file://{index_path}')
    else:
        # This should never happen, since
        # argparse validates this.
        parser.error('Unknown action')


def _add_build_action(subparsers):
    """Setup parsers for 'build' action."""
    parser_build = subparsers.add_parser(
        ACTION_BUILD,
        )

    parser_build.add_argument(
        'packages',
        nargs='+',
        help='List of packages to include',
        #type=lambda string: pc.string_import(string, multiple=True),
        )

    parser_build.add_argument(
        '--browser-dir',
        '-d',
        type=Path,
        help='Output directory',
        default='./build',
        )

def _add_open_action(subparsers):
    """Setup parsers for 'open' action."""
    parser_open = subparsers.add_parser(
        ACTION_OPEN,
        )

    parser_open.add_argument(
        '--browser-dir',
        '-d',
        type=Path,
        help='Module browser directory',
        default='./build',
        )

