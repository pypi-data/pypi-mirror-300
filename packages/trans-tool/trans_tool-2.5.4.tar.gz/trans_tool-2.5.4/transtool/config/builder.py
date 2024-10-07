"""
#
# trans-tool
# The translation files checker and syncing tool.
#
# Copyright ©2021-2024 Marcin Orlowski <MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/trans-tool/
#
"""

import argparse
import re
from pathlib import Path
from typing import List, Optional

from transtool.checks.brackets import Brackets
from transtool.checks.dangling_keys import DanglingKeys
from transtool.checks.empty_translations import EmptyTranslations
from transtool.checks.formatting_values import FormattingValues
from transtool.checks.key_format import KeyFormat
from transtool.checks.missing_translations import MissingTranslations
from transtool.checks.punctuation import Punctuation
from transtool.checks.quotation_marks import QuotationMarks
from transtool.checks.starts_with_the_same_case import StartsWithTheSameCase
from transtool.checks.trailing_white_chars import TrailingWhiteChars
from transtool.checks.substitutions import Substitutions
from transtool.checks.typesetting_quotation_marks import TypesettingQuotationMarks
from transtool.checks.white_chars_before_linefeed import WhiteCharsBeforeLinefeed
from transtool.config.checker_info import CheckerInfo
from transtool.config.config import Config
from transtool.config.reader import ConfigReader
from transtool.const import Const
from transtool.utils import Utils

from simplelog.log import Log


class ConfigBuilder(object):
    """
    A utility class for building and validating a configuration object from various sources including default settings,
    a configuration file, and command line arguments.
    """

    # List of options that can be either turned on or off.
    _on_off_pairs = [
        'color',
        'fatal',
    ]

    _default_checkers = [
        Brackets,
        DanglingKeys,
        EmptyTranslations,
        FormattingValues,
        KeyFormat,
        MissingTranslations,
        Punctuation,
        QuotationMarks,
        StartsWithTheSameCase,
        Substitutions,
        TrailingWhiteChars,
        TypesettingQuotationMarks,
        WhiteCharsBeforeLinefeed,
    ]

    @staticmethod
    def build(config_defaults: Config):
        """
        Constructs a configuration object, populating it first with default checkers, then overriding settings from
        a configuration file (if provided) and command line arguments.

        :param config_defaults: Config object to populate.
        """
        # Let's populate default config with all the supported checkers first
        ConfigBuilder._setup_checkers(config_defaults)

        # Handler CLI args so we can see if there's config file to load
        args = ConfigBuilder._parse_args()
        if args.config_file:
            config_file = Path(args.config_file[0])
            # override with loaded user config file
            config_defaults = ConfigReader().read(config_defaults, config_file)

        # override with command line arguments
        ConfigBuilder._set_from_args(config_defaults, args)

        ConfigBuilder._get_checkers_from_args(config_defaults, args.checkers)

        ConfigBuilder._validate_config(config_defaults)

    @staticmethod
    def _setup_checkers(config: Config, checkers_list: Optional[List[str]] = None) -> None:
        """
        Populates the configuration object with default or specified checkers.
        :param config: Config object to populate.
        :param checkers_list: Optional list of checker classes to use instead of defaults.
        """
        if checkers_list is None:
            checkers_list = ConfigBuilder._default_checkers
        for checker in checkers_list:
            checker_id = checker.__name__
            config.checks[checker_id] = CheckerInfo(checker_id, checker, (checker()).get_default_config())

    @staticmethod
    def _abort(msg: str) -> None:
        """
        Logs an error message and aborts the program.
        :param msg: Error message to log.
        """
        Log.e(msg)
        Utils.abort()

    @staticmethod
    def _validate_config(config: Config) -> None:
        """
        Validates the configuration object, checking languages, separator, and comment marker.
        :param config: Config object to validate.
        """
        if config.languages:
            pattern = re.compile(r'^[a-z]{2,}$')
            for lang in config.languages:
                if not pattern.match(lang):
                    ConfigBuilder._abort(f'Invalid language: "{lang}".')

        if config.separator not in Config.ALLOWED_SEPARATORS:
            ConfigBuilder._abort('Invalid separator character.')

        if config.comment_marker not in Config.ALLOWED_COMMENT_MARKERS:
            ConfigBuilder._abort('Invalid comment marker.')

    @staticmethod
    def _set_on_off_option(config: Config, args, option_name: str) -> None:
        """
        Changes Config's entry if either --<option> or --<no-option> switch is set.
        If none is set, returns Config object unaltered.

        :param config: Config object to modify.
        :param args: Parsed command line arguments.
        :param option_name: Name of the option to set.
        """
        if args.__getattribute__(option_name):
            config.__setattr__(option_name, True)
        elif args.__getattribute__(f'no_{option_name}'):
            config.__setattr__(option_name, False)

    @staticmethod
    def _set_from_args(config: Config, args) -> None:
        """
        Copies settings from parsed command line arguments to the configuration object.

        :param config: Config object to modify.
        :param args: Parsed command line arguments.
        """
        # At this point it is assumed that args are in valid state, i.e. no mutually
        # exclusive options are both set etc.
        for pair_option_name in ConfigBuilder._on_off_pairs:
            ConfigBuilder._set_on_off_option(config, args, pair_option_name)

        # cmd fix
        if args.write_content or args.write_reference:
            args.write = True

        config.write = args.write
        config.write_content = args.write_content
        config.write_reference = args.write_reference

        # Set optional args, if set by user.
        optionals = [
            'separator',
            'comment_marker',
            'quiet',
            'verbose',
            'file_suffix',
        ]
        for option_name in optionals:
            opt_val = args.__getattribute__(option_name)
            if opt_val is not None:
                config.__setattr__(option_name, opt_val)

        # languages
        if args.languages:
            for lang in args.languages:
                for sub_lang in lang.split():
                    Utils.add_if_not_in_list(config.languages, sub_lang)
        if args.languages_skip:
            for lang_skip in args.languages_skip:
                for sub_lang_skip in lang_skip.split():
                    Utils.add_if_not_in_list(config.languages_skip, sub_lang_skip)

        # base files
        if args.files:
            ConfigBuilder._add_file_suffix(config, args.files)
            Utils.add_if_not_in_list(config.files, args.files)

    @staticmethod
    def _get_checkers_from_args(config: Config, args_checkers: Optional[List[str]]) -> None:
        """
        If `--checks` argument list is provided, used checkers will be adjusted according to
        values (Checker IDs) provided.

        :param config: Config object to modify.
        :param args_checkers: List of checker IDs from command line arguments.
        """
        all_checkers = {checker.__name__.lower(): checker for checker in ConfigBuilder._default_checkers}
        if args_checkers:
            checkers = []
            for checker_id in args_checkers:
                if checker_id.lower() not in all_checkers:
                    ConfigBuilder._abort(f'Unknown checker ID "{checker_id}".')
                Utils.add_if_not_in_list(checkers, checker_id)
            ConfigBuilder._setup_checkers(config, checkers)

    @staticmethod
    def _add_file_suffix(config: Config, files: Optional[List[Path]]) -> None:
        """
        Ensures the specified files have the correct suffix.

        :param config: Config object to use for retrieving the required file suffix.
        :param files: List of file paths to modify.
        """
        if files:
            suffix_len = len(config.file_suffix)
            for idx, file in enumerate(files):
                # 'PosixPath' object cannot be sliced.
                path_str = str(file)
                if path_str[suffix_len * -1:] != config.file_suffix:
                    files[idx] = Path(f'{path_str}{config.file_suffix}')

    @staticmethod
    def _parse_args() -> argparse:
        """
        Parses command line arguments using argparse.

        :return: argparse.Namespace object containing parsed arguments.

        When you add new argparse based option to the tool, you need to:
        * add a proper entry to the argument group, with correct key and type,
        * Edit Config class and ensure new option is mapped to Config attribute.
        * Update `_set_from_args()` method to copy data to Config instance.
        * for entries used for argparse that should not be part of Config object, you need to exclude them, so tests
        checking for Config <-> args match won't fail
        * Edit FakeArgs class (of TestConfigBuilder test class) and ensure it matches edited Config (there are tests
        that should detect if something is wrong, so always run unit tests!).
        """
        parser = argparse.ArgumentParser(prog=Const.APP_NAME.lower(), formatter_class=argparse.RawTextHelpFormatter,
                                         description='\n'.join(Const.APP_DESCRIPTION))

        group = parser.add_argument_group('Base options')
        group.add_argument('--config', action='store', dest='config_file', nargs=1, metavar='FILE',
                           help='Use specified config file. Command line arguments override config settings.')
        group.add_argument('--config-dump', action='store_true', dest='config_dump',
                           help='Print config as seen by the app once config file and args are parsed.')
        group.add_argument('-b', '--base', action='store', dest='files', nargs='+', metavar='FILE',
                           help='List of base files to check.')
        group.add_argument('-l', '--lang', action='store', dest='languages', nargs='+', metavar='LANG',
                           help='List of languages to check (space or comma separated if more than one, i.e. "de pl").')
        group.add_argument('-ls', '--lang-skip', action='store', dest='languages_skip', nargs='+', metavar='LANG',
                           help='List of languages to ignore. This overrides languages provided by `--lang` '
                                + ' (which can be sourced from application config file).')

        group = parser.add_argument_group('Additional options')
        group.add_argument('-w', '--write', action='store_true', dest='write',
                           help='Creates or Updates existing translation files in-place using base file as reference.')
        group.add_argument('-wc', '--write-content', action='store_true', dest='write_content',
                           help='Non existing translations are writted with default value taken from base file.')
        group.add_argument('-wr', '--write-ref', action='store_true', dest='write_reference',
                           help='Includes comments with reference values from base string for every translation entry.')
        group.add_argument('--separator', action='store', dest='separator', metavar='CHAR', nargs=1,
                           help='If specified, only given CHAR is considered a valid key/value separator.'
                                + f'Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')
        group.add_argument('--comment', action='store', dest='comment_marker', metavar='CHAR', nargs=1,
                           help='If specified, only given CHAR is considered valid comment marker.'
                                + f'Must be one of the following: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')
        group.add_argument('--suffix', action='store', dest='file_suffix', metavar='STRING', nargs=1,
                           help=f'Default file name suffix. Default: "{Config.DEFAULT_FILE_SUFFIX}".')

        group = parser.add_argument_group('Checks controlling options')
        group.add_argument('--checks', action='store', dest='checkers', nargs='+', metavar='CHECK_ID',
                           help='List of checks ID to be executed. By default all available checks are run.')

        group.add_argument('-f', '--fatal', action='store_true', dest='fatal',
                           help='Enables strict mode. All warnings are treated as errors and are fatal.')
        group.add_argument('-nf', '--no-fatal', action='store_true', dest='no_fatal',
                           help='Warnings are non-fatal, errors are fatal (default).')

        group = parser.add_argument_group('Application controls')
        group.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                           help='Enables quiet mode, muting all output but fatal errors.')
        group.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                           help='Produces more verbose reports.')
        group.add_argument('-d', '--debug', action='store_true', dest='debug',
                           help='Enables debug output.')

        group.add_argument('-c', '--color', action='store_true', dest='color',
                           help='Enables use of ANSI colors (default).')
        group.add_argument('-nc', '--no-color', action='store_true', dest='no_color',
                           help='Disables use of ANSI colors.')

        group = parser.add_argument_group('Misc')
        group.add_argument('--version', action='store_true', dest='show_version',
                           help='Displays application version details and quits.')

        args = parser.parse_args()

        # If user separated languages with comma instead of space, lets do some magic for it to work too.
        args.languages = ConfigBuilder._process_comma_separated_langs(args.languages)

        ConfigBuilder._validate_args(args)

        return args

    @staticmethod
    def _process_comma_separated_langs(languages: Optional[List[str]]) -> Optional[List[str]]:
        """
        Processes language arguments, splitting comma-separated values into separate strings.

        :param languages: List of language codes, potentially comma-separated.
        :return: Processed list of language codes.
        """
        if languages is None:
            return None

        result = []
        for lang in languages:
            tmp = lang.split(',')
            if len(tmp) > 1:
                _ = [result.append(code) for code in tmp if code.strip() != '']  # noqa: WPS122
            else:
                result.append(lang)

        return result

    @staticmethod
    def _validate_args(args):
        """
        Validates the parsed command line arguments for mutual exclusivity and other conditions.

        :param args: argparse.Namespace object containing parsed arguments.
        """
        # Check use of mutually exclusive pairs
        for option_name in ConfigBuilder._on_off_pairs:
            if args.__getattribute__(option_name) and args.__getattribute__(f'no_{option_name}'):
                ConfigBuilder._abort(f'You cannot use "--{option_name}" and "--no-{option_name}" at the same time.')

        # --quiet vs --verbose
        if args.__getattribute__('quiet') and args.__getattribute__('verbose'):
            ConfigBuilder._abort('You cannot enable "quiet" and "verbose" options both at the same time.')

        # Separator character.
        if args.separator and args.separator not in Config.ALLOWED_SEPARATORS:
            ConfigBuilder._abort(
                f'Invalid separator. Must be one of the following: {", ".join(Config.ALLOWED_SEPARATORS)}')

        # Comment marker character.
        if args.comment_marker and args.comment_marker not in Config.ALLOWED_COMMENT_MARKERS:
            ConfigBuilder._abort(f'Invalid comment marker. Must be one of: {", ".join(Config.ALLOWED_COMMENT_MARKERS)}')
