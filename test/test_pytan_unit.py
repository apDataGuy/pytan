#!/usr/bin/env python -ttB
"""
This contains unit tests for pytan.

These unit tests do not require a connection to a Tanium server in order to run.
"""
import sys

# disable python from creating .pyc files everywhere
sys.dont_write_bytecode = True

import os
import unittest
import json

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
root_dir = os.path.join(my_dir, os.pardir)
root_dir = os.path.abspath(root_dir)
lib_dir = os.path.join(root_dir, 'lib')
path_adds = [my_dir, lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import pytan
import taniumpy
from pytan import utils
from pytan import constants
from pytan.utils import HumanParserError
from pytan.utils import DefinitionParserError
from pytan.utils import HandlerError

# control the amount of output from unittests
TESTVERBOSITY = 1

# have unittest exit immediately on unexpected error
FAILFAST = True

# catch control-C to allow current test suite to finish (press 2x to force)
CATCHBREAK = True

# set logging for all logs in pytan to same level as TESTVERBOSITY
utils.setup_console_logging()
utils.set_log_levels(TESTVERBOSITY)


class TestDehumanizeSensorUtils(unittest.TestCase):
    def test_single_str(self):
        sensors = 'Sensor1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'name': 'Sensor1'}]
        self.assertEquals(sensor_defs, exp)

    def test_single_str_with_filter(self):
        sensors = 'Sensor1, that is:.*'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {},
                'name': 'Sensor1',
                'options': {}
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_single_str_complex1(self):
        sensors = (
            'Sensor1, that is:.*, opt:value_type:string, opt:ignore_case, '
            'opt:max_data_age:3600, opt:match_any_value'
        )
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {},
                'name': 'Sensor1',
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0
                }
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_single_str_complex2(self):
        sensors = (
            'Sensor1{k1=v1,k2=v2}, that is:.*, opt:value_type:string, '
            'opt:ignore_case, opt:max_data_age:3600, opt:match_any_value'
        )
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {
                    'not_flag': 0,
                    'operator': 'RegexMatch',
                    'value': '.*'
                },
                'name': 'Sensor1',
                'options': {
                    'all_times_flag': 0,
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string'
                },
                'params': {'k1': 'v1', 'k2': 'v2'}
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_multi_list_complex(self):
        sensors = [
            'Computer Name',
            'id:1',
            'Operating System, that contains:Windows',
            ('Sensor1{k1=v1,k2=v2}, that is:.*, opt:value_type:string, '
             'opt:ignore_case, opt:max_data_age:3600, opt:match_any_value'),
        ]
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [
            {
                'filter': {},
                'params': {},
                'name': 'Computer Name',
                'options': {}
            },
            {
                'filter': {},
                'params': {},
                'id': '1',
                'options': {}
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*Windows.*'
                },
                'params': {},
                'name': 'Operating System',
                'options': {}
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {'k2': 'v2', 'k1': 'v1'},
                'name': 'Sensor1',
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0
                }
            }
        ]
        self.assertEquals(sensor_defs, exp)

    def test_valid_simple_str_id_selector(self):
        sensors = 'id:1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'id': '1'}]
        self.assertEquals(sensor_defs, exp)

    def test_valid_simple_str_hash_selector(self):
        sensors = 'hash:1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'hash': '1'}]
        self.assertEquals(sensor_defs, exp)

    def test_valid_simple_str_name_selector(self):
        sensors = 'name:Sensor1'
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'name': 'Sensor1'}]
        self.assertEquals(sensor_defs, exp)

    def test_valid_simple_list(self):
        sensors = ['Sensor1']
        sensor_defs = utils.dehumanize_sensors(sensors)
        exp = [{'filter': {}, 'params': {}, 'options': {}, 'name': 'Sensor1'}]
        self.assertEquals(sensor_defs, exp)

    def test_empty_args_str(self):
        e = "A string or list of strings must be supplied as 'sensors'!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.dehumanize_sensors('')

    def test_empty_args_list(self):
        e = "A string or list of strings must be supplied as 'sensors'!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.dehumanize_sensors([])

    def test_empty_args_dict(self):
        e = "A string or list of strings must be supplied as 'sensors'!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.dehumanize_sensors({})


class TestDehumanizeQuestionFilterUtils(unittest.TestCase):
    def test_single_filter_str(self):
        question_filters = 'Sensor1, that contains:Windows'
        question_filter_defs = utils.dehumanize_question_filters(
            question_filters
        )
        exp = [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*Windows.*'
                },
                'name': 'Sensor1'
            }
        ]
        self.assertEquals(question_filter_defs, exp)

    def test_single_filter_list(self):
        question_filters = ['Sensor1, that contains:Windows']
        question_filter_defs = utils.dehumanize_question_filters(
            question_filters
        )
        exp = [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*Windows.*'
                },
                'name': 'Sensor1'
            }
        ]
        self.assertEquals(question_filter_defs, exp)

    def test_multi_filter_list(self):
        question_filters = [
            'Sensor1, that contains:Windows',
            'Sensor2, that does not contain:10.10.10.10',
        ]
        question_filter_defs = utils.dehumanize_question_filters(
            question_filters
        )
        exp = [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*Windows.*'
                },
                'name': 'Sensor1'
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 1,
                    'value': '.*10.10.10.10.*'
                },
                'name': 'Sensor2'
            }
        ]
        self.assertEquals(question_filter_defs, exp)

    def test_empty_filterstr(self):
        question_filters = ''
        question_filter_defs = utils.dehumanize_question_filters(
            question_filters
        )
        exp = []
        self.assertEquals(question_filter_defs, exp)

    def test_empty_filterlist(self):
        question_filters = []
        question_filter_defs = utils.dehumanize_question_filters(
            question_filters
        )
        exp = []
        self.assertEquals(question_filter_defs, exp)

    def test_invalid_filter1(self):
        o = 'Sensor1, that feels:funny'
        e = "Filter .* is not a valid filter!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.dehumanize_question_filters(o)

    def test_invalid_filter2(self):
        o = 'Sensor1'
        e = "Filter .* is not a valid filter!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.dehumanize_question_filters(o)

    def test_invalid_filter3(self):
        o = 'Sensor1, th'
        e = "Filter .* is not a valid filter!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.dehumanize_question_filters(o)


class TestDehumanizeQuestionOptionUtils(unittest.TestCase):
    def test_empty_optionstr(self):
        question_options = ''
        question_option_defs = utils.dehumanize_question_options(
            question_options
        )
        exp = {}
        self.assertEquals(question_option_defs, exp)

    def test_empty_optionlist(self):
        question_options = []
        question_option_defs = utils.dehumanize_question_options(
            question_options
        )
        exp = {}
        self.assertEquals(question_option_defs, exp)

    def test_option_str(self):
        question_options = 'ignore_case'
        question_option_defs = utils.dehumanize_question_options(
            question_options
        )
        exp = {'ignore_case_flag': 1}
        self.assertEquals(question_option_defs, exp)

    def test_option_list_single(self):
        question_options = ['ignore_case']
        question_option_defs = utils.dehumanize_question_options(
            question_options
        )
        exp = {'ignore_case_flag': 1}
        self.assertEquals(question_option_defs, exp)

    def test_option_list_multi(self):
        question_options = ['ignore_case', 'and']
        question_option_defs = utils.dehumanize_question_options(
            question_options
        )
        exp = {'ignore_case_flag': 1, 'and_flag': 1}
        self.assertEquals(question_option_defs, exp)

    def test_option_list_many(self):
        question_options = [
            'ignore_case', 'and', 'value_type:string', 'max_data_age:3600',
        ]
        question_option_defs = utils.dehumanize_question_options(
            question_options
        )
        exp = {
            'value_type': 'string',
            'ignore_case_flag': 1,
            'max_age_seconds': '3600',
            'and_flag': 1
        }
        self.assertEquals(question_option_defs, exp)

    def test_invalid_option1(self):
        o = 'willy wonka'
        e = "Option '{}' is not a valid option!".format(o)
        with self.assertRaisesRegexp(HumanParserError, e):
            question_options = [o]
            utils.dehumanize_question_options(question_options)

    def test_invalid_option2(self):
        o = 'willy wonka'
        e = "Option '{}' is not a valid option!".format(o)
        with self.assertRaisesRegexp(HumanParserError, e):
            question_options = o
            utils.dehumanize_question_options(question_options)


class TestDehumanizeExtractionUtils(unittest.TestCase):
    def test_extract_selector(self):
        s = 'id:1 more:stuff,here'
        exp = ('1 more:stuff,here', 'id')
        self.assertEquals(utils.extract_selector(s), exp)

    def test_extract_selector_use_name_if_noselector(self):
        s = 'Sensor1 more:stuff,here'
        exp = ('Sensor1 more:stuff,here', 'name')
        r = utils.extract_selector(s)
        self.assertEquals(r, exp)

    def test_extract_params(self):
        s = 'Sensor1{k1=v1,k2=v2}, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {'k2': 'v2', 'k1': 'v1'})
        r = utils.extract_params(s)
        self.assertEquals(r, exp)

    def test_extract_params_noparams(self):
        s = 'Sensor1, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {})
        r = utils.extract_params(s)
        self.assertEquals(r, exp)

    def test_extract_options_single(self):
        s = 'Sensor1, more:stuff,here, opt:ignore_case'
        exp = ('Sensor1, more:stuff,here', {'ignore_case_flag': 1})
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    def test_extract_options_many(self):
        s = (
            'Sensor1, more:stuff,here, opt:ignore_case, opt:max_data_age:3600'
            ', opt:match_any_value, opt:value_type:string'
        )
        exp = (
            'Sensor1, more:stuff,here',
            {
                'value_type': 'string',
                'ignore_case_flag': 1,
                'max_age_seconds': '3600',
                'all_values_flag': 0,
                'all_times_flag': 0
            }
        )
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    def test_extract_options_nooptions(self):
        s = 'Sensor1, more:stuff,here'
        exp = ('Sensor1, more:stuff,here', {})
        r = utils.extract_options(s)
        self.assertEquals(r, exp)

    def test_extract_filter_valid(self):
        s = 'Sensor1, that is:.*'
        exp = (
            'Sensor1',
            {'operator': 'RegexMatch', 'not_flag': 0, 'value': '.*'}
        )
        r = utils.extract_filter(s)
        self.assertEquals(r, exp)

    def test_extract_filter_valid_all(self):
        for x in constants.FILTER_MAPS:
            for y in x['human']:
                z = utils.extract_filter('Sensor1, that {}:test value'.format(y))
                self.assertTrue(z)
                self.assertEquals(len(z), 2)
                self.assertEquals(z[0], 'Sensor1')
                self.assertIn('test value', z[1]['value'])

    def test_extract_filter_nofilter(self):
        s = 'Sensor1'
        exp = ('Sensor1', {})
        r = utils.extract_filter(s)
        self.assertEquals(r, exp)

    def test_extract_params_multiparams(self):
        s = 'Sensor1{k1=v1,k2=v2}{}, more:stuff,here'
        e = "More than one parameter \(\{\}\) passed in '.*'"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.extract_params(s)

    def test_extract_params_missing_seperator(self):
        s = 'Sensor1{v1,v2}, more:stuff,here'
        e = "Parameter v1 missing key/value seperator \(=\)"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.extract_params(s)

    def test_extract_options_missing_value_max_data_age(self):
        s = 'Sensor1, more:stuff,here, opt:max_data_age'
        e = (
            "Option 'max_data_age' is missing a <type 'int'> value of seconds"
            ".*"
        )
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.extract_options(s)

    def test_extract_options_missing_value_value_type(self):
        s = 'Sensor1, more:stuff,here, opt:value_type'
        e = (
            "Option 'value_type' is missing a <type 'str'> value of "
            "value_type.*"
        )
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.extract_options(s)

    def test_extract_options_invalid_option(self):
        s = 'Sensor1, more:stuff,here, opt:invalid_option'
        e = "Option 'invalid_option' is not a valid option!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.extract_options(s)

    def test_extract_filter_invalid(self):
        s = 'Sensor1, that meets:.*'
        e = "Filter .* is not a valid filter!"
        with self.assertRaisesRegexp(HumanParserError, e):
            utils.extract_filter(s)


class TestManualSensorDefParseUtils(unittest.TestCase):
    def test_parse_str1(self):
        '''simple str is parsed into list of same str'''
        kwargs = {'sensor_defs': 'Sensor1'}
        r = utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=False,
            **kwargs
        )
        exp = [{'name': 'Sensor1'}]
        self.assertEquals(r, exp)

    def test_parse_dict_name(self):
        '''dict with name is parsed into list of same dict'''
        kwargs = {'sensor_defs': {'name': 'Sensor1'}}
        r = utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=False,
            **kwargs
        )
        exp = [{'name': 'Sensor1'}]
        self.assertEquals(r, exp)

    def test_parse_dict_id(self):
        '''dict with id is parsed into list of same dict'''
        kwargs = {'sensor_defs': {'id': '1'}}
        r = utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=False,
            **kwargs
        )
        exp = [{'id': '1'}]
        self.assertEquals(r, exp)

    def test_parse_dict_hash(self):
        '''dict with hash is parsed into list of same dict'''
        kwargs = {'sensor_defs': {'hash': '1'}}
        r = utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=False,
            **kwargs
        )
        exp = [{'hash': '1'}]
        self.assertEquals(r, exp)

    def test_parse_complex(self):
        '''list with many items is parsed into same list'''
        sensor_defs = [
            {
                'filter': {},
                'params': {},
                'name': 'Computer Name',
                'options': {}
            },
            {
                'filter': {},
                'params': {},
                'id': '1',
                'options': {}
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*Windows.*'
                },
                'params': {},
                'name': 'Operating System',
                'options': {}
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {'k2': 'v2', 'k1': 'v1'},
                'name': 'Sensor1',
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0
                }
            }
        ]
        kwargs = {'sensor_defs': sensor_defs}

        r = utils.parse_defs(
            defname='sensor_defs',
            deftypes=['list()', 'str()', 'dict()'],
            strconv='name',
            empty_ok=False,
            **kwargs
        )
        self.assertEquals(r, sensor_defs)

    def test_parse_noargs(self):
        '''no args throws exception'''
        kwargs = {}
        e = (
            "'sensor_defs' requires a non-empty value of type: list\(\) or "
            "str\(\) or dict\(\)"
        )
        with self.assertRaisesRegexp(DefinitionParserError, e):
            utils.parse_defs(
                defname='sensor_defs',
                deftypes=['list()', 'str()', 'dict()'],
                strconv='name',
                empty_ok=False,
                **kwargs
            )

    def test_parse_none(self):
        '''args==None throws exception'''
        e = (
            "'sensor_defs' requires a non-empty value of type: list\(\) or "
            "str\(\) or dict\(\)"
        )
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': None}
            utils.parse_defs(
                defname='sensor_defs',
                deftypes=['list()', 'str()', 'dict()'],
                strconv='name',
                empty_ok=False,
                **kwargs
            )

    def test_parse_emptystr(self):
        '''args=='' throws exception'''
        e = (
            "'sensor_defs' requires a non-empty value of type: list\(\) or "
            "str\(\) or dict\(\)"
        )
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': ''}
            utils.parse_defs(
                defname='sensor_defs',
                deftypes=['list()', 'str()', 'dict()'],
                strconv='name',
                empty_ok=False,
                **kwargs
            )

    def test_parse_emptylist(self):
        '''args==[] throws exception'''
        e = (
            "'sensor_defs' requires a non-empty value of type: list\(\) or "
            "str\(\) or dict\(\)"
        )
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': []}
            utils.parse_defs(
                defname='sensor_defs',
                deftypes=['list()', 'str()', 'dict()'],
                strconv='name',
                empty_ok=False,
                **kwargs
            )

    def test_parse_emptydict(self):
        '''args=={} throws exception'''
        e = (
            "'sensor_defs' requires a non-empty value of type: list\(\) or "
            "str\(\) or dict\(\)"
        )
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': {}}
            utils.parse_defs(
                defname='sensor_defs',
                deftypes=['list()', 'str()', 'dict()'],
                strconv='name',
                empty_ok=False,
                **kwargs
            )


class TestManualQuestionFilterDefParseUtils(unittest.TestCase):
    def test_parse_noargs(self):
        kwargs = {}
        r = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_none(self):
        kwargs = {'question_filter_defs': None}
        r = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_emptystr(self):
        kwargs = {'question_filter_defs': ''}
        r = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_emptylist(self):
        kwargs = {'question_filter_defs': []}
        r = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_emptydict(self):
        kwargs = {'question_filter_defs': {}}
        r = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_single_filter(self):
        kwargs = {'question_filter_defs': {
            'filter': {
                'operator': 'RegexMatch',
                'not_flag': 0,
                'value': '.*Windows.*'
            },
            'name': 'Operating System',
        }}
        r = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertEquals(r, [kwargs['question_filter_defs']])

    def test_parse_multi_filter(self):
        kwargs = {'question_filter_defs': [
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*Windows.*'
                },
                'name': 'Operating System',
            },
            {
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 1,
                    'value': '.*Linux.*'
                },
                'name': 'Operating System',
            },
        ]}
        r = utils.parse_defs(
            defname='question_filter_defs',
            deftypes=['list()', 'dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertEquals(r, kwargs['question_filter_defs'])

    def test_parse_str(self):
        e = (
            "Argument 'question_filter_defs' has an invalid type "
            "<type 'str'>"
        )
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'question_filter_defs': 'no string allowed'}
            utils.parse_defs(
                defname='question_filter_defs',
                deftypes=['list()', 'dict()'],
                empty_ok=True,
                **kwargs
            )


class TestManualQuestionOptionDefParseUtils(unittest.TestCase):
    def test_parse_noargs(self):
        kwargs = {}
        r = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_none(self):
        kwargs = {'question_option_defs': None}
        r = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_emptystr(self):
        kwargs = {'question_option_defs': ''}
        r = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_emptylist(self):
        kwargs = {'question_option_defs': []}
        r = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_emptydict(self):
        kwargs = {'question_option_defs': {}}
        r = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertFalse(r)

    def test_parse_options_dict(self):
        kwargs = {'question_option_defs': {
            'all_values_flag': 0,
            'ignore_case_flag': 1,
            'max_age_seconds': '3600',
            'value_type': 'string',
            'all_times_flag': 0
        }}
        r = utils.parse_defs(
            defname='question_option_defs',
            deftypes=['dict()'],
            empty_ok=True,
            **kwargs
        )
        self.assertEquals(r, kwargs['question_option_defs'])

    def test_parse_str(self):
        e = (
            "'question_option_defs' requires a non-empty value of type:"
            " dict\(\)"
        )
        kwargs = {'question_option_defs': 'no string allowed'}
        with self.assertRaisesRegexp(DefinitionParserError, e):
            utils.parse_defs(
                defname='question_option_defs',
                deftypes=['dict()'],
                empty_ok=True,
                **kwargs
            )

    def test_parse_list(self):
        e = (
            "'question_option_defs' requires a non-empty value of type:"
            " dict\(\)"
        )
        kwargs = {'question_option_defs': ['no list allowed']}
        with self.assertRaisesRegexp(DefinitionParserError, e):
            utils.parse_defs(
                defname='question_option_defs',
                deftypes=['dict()'],
                empty_ok=True,
                **kwargs
            )


class TestManualPackageDefValidateUtils(unittest.TestCase):
    def test_valid1(self):
        kwargs = {'package_def': {'name': 'Package1'}}
        utils.val_package_def(**kwargs)

    def test_valid2(self):
        kwargs = {'package_def': {
            'name': 'Package1',
            'params': {'dirname': 'Program Files'},
        }}
        utils.val_package_def(**kwargs)

    def test_invalid1(self):
        e = "Package definition.*missing one of id, name!"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'package_def': {'NONAME': 'Package1'}}
            utils.val_package_def(**kwargs)

    def test_invalid2(self):
        e = "Package definition.*has more than one of id, name!"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'package_def': {'name': 'test1', 'id': '2'}}
            utils.val_package_def(**kwargs)


class TestManualSensorDefValidateUtils(unittest.TestCase):
    def test_valid1(self):
        kwargs = {'sensor_defs': [{'name': 'Sensor1'}]}
        utils.val_sensor_defs(**kwargs)

    def test_valid2(self):
        kwargs = {'sensor_defs': [
            {
                'name': 'Sensor1',
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
            }
        ]}
        utils.val_sensor_defs(**kwargs)

    def test_valid3(self):
        kwargs = {'sensor_defs': [
            {
                'name': 'Sensor1',
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0
                },
            }
        ]}
        utils.val_sensor_defs(**kwargs)

    def test_valid4(self):
        kwargs = {'sensor_defs': [{'name': 'test1', 'filter': {'n': 'k'}}]}
        utils.val_sensor_defs(**kwargs)

    def test_invalid1(self):
        e = "Sensor definition.*missing one of id, name, hash!"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': [{'NONAME': 'Sensor1'}]}
            utils.val_sensor_defs(**kwargs)

    def test_invalid2(self):
        e = "Sensor definition.*missing one of id, name, hash!"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': [{}]}
            utils.val_sensor_defs(**kwargs)

    def test_invalid3(self):
        e = (
            "'filter' key in definition dictionary must be a \[<type 'dict'>\]"
            ", you supplied a <type 'list'>!"
        )
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': [{'name': 'test1', 'filter': [{}]}]}
            utils.val_sensor_defs(**kwargs)

    def test_invalid4(self):
        e = "Sensor definition.*has more than one of id, name, hash!"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'sensor_defs': [{'name': 'test1', 'id': '2'}]}
            utils.val_sensor_defs(**kwargs)


class TestManualQuestionFilterDefValidateUtils(unittest.TestCase):
    def test_valid1(self):
        kwargs = {'q_filter_defs': [
            {
                'name': 'Sensor1',
                'filter': {
                    'operator': 'RegexMatch',
                    'not_flag': 0,
                    'value': '.*'
                },
            }
        ]}
        utils.val_q_filter_defs(**kwargs)

    def test_valid2(self):
        kwargs = {'q_filter_defs': []}
        utils.val_q_filter_defs(**kwargs)

    def test_invalid1(self):
        e = "Definition.*missing 'filter' key!"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            kwargs = {'q_filter_defs': [{'name': 'Sensor1'}]}
            utils.val_q_filter_defs(**kwargs)


class TestManualBuildObjectUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls): # noqa
        def load_sensor(n):
            sensor_obj_json_path = os.path.join(my_dir, n)
            sensor_obj_json = json.load(open(sensor_obj_json_path))
            return taniumpy.BaseType.from_jsonable(sensor_obj_json)

        # load in our JSON sensor object for testing
        cls.sensor_obj_with_params = load_sensor('sensor_obj_with_params.json')
        cls.sensor_obj_no_params = load_sensor('sensor_obj_no_params.json')

    def test_build_selectlist_obj_noparamssensorobj_noparams(self):
        '''builds a selectlist object using a sensor obj with no params'''

        sensor_defs = [
            {
                'name': 'Fake Sensor',
                'filter': {
                    'operator': 'regexmatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0,
                    'ignored_option': 'tt',
                },
                'sensor_obj': self.sensor_obj_no_params
            }
        ]

        kwargs = {'sensor_defs': sensor_defs}

        r = utils.build_selectlist_obj(**kwargs)

        self.assertIsInstance(r, taniumpy.SelectList)
        self.assertIsInstance(r.select[0], taniumpy.Select)
        self.assertEqual(len(r.select), 1)
        self.assertIsInstance(r.select[0].filter, taniumpy.Filter)
        self.assertIsInstance(r.select[0].sensor, taniumpy.Sensor)
        self.assertEqual(
            r.select[0].sensor.hash, self.sensor_obj_no_params.hash)
        self.assertEqual(
            r.select[0].filter.sensor.hash, self.sensor_obj_no_params.hash)
        self.assertIsNone(r.select[0].sensor.parameters)
        self.assertEqual(r.select[0].filter.operator, 'RegexMatch')
        self.assertEqual(r.select[0].filter.not_flag, 0)
        self.assertEqual(r.select[0].filter.value, '.*')
        self.assertEqual(r.select[0].filter.all_values_flag, 0)
        self.assertEqual(r.select[0].filter.ignore_case_flag, 1)
        self.assertEqual(r.select[0].filter.max_age_seconds, 3600)
        self.assertEqual(r.select[0].filter.value_type, 'String')
        self.assertEqual(r.select[0].filter.all_times_flag, 0)
        self.assertFalse(hasattr(r.select[0].filter, 'ignored_option'))

    def test_build_selectlist_obj_noparamssensorobj_withparams(self):
        '''builds a selectlist object using a sensor obj with no params,
        but passing in params (which should be added as of 1.0.4)'''

        sensor_defs = [
            {
                'name': 'Fake Sensor',
                'filter': {
                    'operator': 'regexmatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {
                    'dirname': 'Program Files',
                },
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0,
                    'ignored_option': 'tt',
                },
                'sensor_obj': self.sensor_obj_no_params
            }
        ]

        kwargs = {'sensor_defs': sensor_defs}

        r = utils.build_selectlist_obj(**kwargs)
        print r.to_json(r)
        self.assertIsInstance(r, taniumpy.SelectList)
        self.assertIsInstance(r.select[0], taniumpy.Select)
        self.assertEqual(len(r.select), 1)
        self.assertIsInstance(r.select[0].filter, taniumpy.Filter)
        self.assertIsInstance(r.select[0].sensor, taniumpy.Sensor)
        self.assertEqual(
            r.select[0].sensor.source_id, self.sensor_obj_no_params.id)
        self.assertEqual(
            r.select[0].filter.sensor.id, self.sensor_obj_no_params.id)
        self.assertTrue(r.select[0].sensor.parameters)
        self.assertEqual(r.select[0].filter.operator, 'RegexMatch')
        self.assertEqual(r.select[0].filter.not_flag, 0)
        self.assertEqual(r.select[0].filter.value, '.*')
        self.assertEqual(r.select[0].filter.all_values_flag, 0)
        self.assertEqual(r.select[0].filter.ignore_case_flag, 1)
        self.assertEqual(r.select[0].filter.max_age_seconds, 3600)
        self.assertEqual(r.select[0].filter.value_type, 'String')
        self.assertEqual(r.select[0].filter.all_times_flag, 0)
        self.assertFalse(hasattr(r.select[0].filter, 'ignored_option'))

    def test_build_selectlist_obj_withparamssensorobj_noparams(self):
        '''builds a selectlist object using a sensor obj with 4 params
        but not supplying any values for any of the params'''

        sensor_defs = [
            {
                'name': 'Fake Sensor',
                'filter': {
                    'operator': 'regexmatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0,
                    'ignored_option': 'tt',
                },
                'sensor_obj': self.sensor_obj_with_params
            }
        ]

        kwargs = {'sensor_defs': sensor_defs}

        r = utils.build_selectlist_obj(**kwargs)

        self.assertIsInstance(r, taniumpy.SelectList)
        self.assertIsInstance(r.select[0], taniumpy.Select)
        self.assertEqual(len(r.select), 1)
        self.assertIsInstance(r.select[0].filter, taniumpy.Filter)
        self.assertIsInstance(r.select[0].sensor, taniumpy.Sensor)
        self.assertEqual(
            r.select[0].sensor.source_id, self.sensor_obj_with_params.id)
        self.assertEqual(
            r.select[0].filter.sensor.id, self.sensor_obj_with_params.id)
        self.assertEqual(len(r.select[0].sensor.parameters), 4)
        for x in r.select[0].sensor.parameters:
            self.assertRegexpMatches(x.key, '||.*||')
            if x.key == '||dirname||':
                self.assertEqual(x.value, '')
            if x.key == '||regexp||':
                self.assertEqual(x.value, '')
            if x.key == '||casesensitive||':
                self.assertEqual(x.value, 'No')
            if x.key == '||global||':
                self.assertEqual(x.value, 'No')

        self.assertEqual(r.select[0].filter.operator, 'RegexMatch')
        self.assertEqual(r.select[0].filter.not_flag, 0)
        self.assertEqual(r.select[0].filter.value, '.*')
        self.assertEqual(r.select[0].filter.all_values_flag, 0)
        self.assertEqual(r.select[0].filter.ignore_case_flag, 1)
        self.assertEqual(r.select[0].filter.max_age_seconds, 3600)
        self.assertEqual(r.select[0].filter.value_type, 'String')
        self.assertEqual(r.select[0].filter.all_times_flag, 0)
        self.assertFalse(hasattr(r.select[0].filter, 'ignored_option'))

    def test_build_selectlist_obj_withparamssensorobj_withparams(self):
        '''builds a selectlist object using a sensor obj with 4 params
        but supplying a value for only one param'''

        sensor_defs = [
            {
                'name': 'Fake Sensor',
                'filter': {
                    'operator': 'regexmatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'params': {
                    'dirname': 'Program Files',
                },
                'options': {
                    'all_values_flag': 0,
                    'ignore_case_flag': 1,
                    'max_age_seconds': '3600',
                    'value_type': 'string',
                    'all_times_flag': 0,
                    'ignored_option': 'tt',
                },
                'sensor_obj': self.sensor_obj_with_params
            }
        ]

        kwargs = {'sensor_defs': sensor_defs}

        r = utils.build_selectlist_obj(**kwargs)

        self.assertIsInstance(r, taniumpy.SelectList)
        self.assertIsInstance(r.select[0], taniumpy.Select)
        self.assertEqual(len(r.select), 1)
        self.assertIsInstance(r.select[0].filter, taniumpy.Filter)
        self.assertIsInstance(r.select[0].sensor, taniumpy.Sensor)
        self.assertEqual(
            r.select[0].sensor.source_id, self.sensor_obj_with_params.id)
        self.assertEqual(
            r.select[0].filter.sensor.id, self.sensor_obj_with_params.id)

        self.assertEqual(len(r.select[0].sensor.parameters), 4)
        for x in r.select[0].sensor.parameters:
            self.assertRegexpMatches(x.key, '||.*||')
            if x.key == '||dirname||':
                self.assertEqual(x.value, 'Program Files')
            if x.key == '||regexp||':
                self.assertEqual(x.value, '')
            if x.key == '||casesensitive||':
                self.assertEqual(x.value, 'No')
            if x.key == '||global||':
                self.assertEqual(x.value, 'No')

        self.assertEqual(r.select[0].filter.operator, 'RegexMatch')
        self.assertEqual(r.select[0].filter.not_flag, 0)
        self.assertEqual(r.select[0].filter.value, '.*')
        self.assertEqual(r.select[0].filter.all_values_flag, 0)
        self.assertEqual(r.select[0].filter.ignore_case_flag, 1)
        self.assertEqual(r.select[0].filter.max_age_seconds, 3600)
        self.assertEqual(r.select[0].filter.value_type, 'String')
        self.assertEqual(r.select[0].filter.all_times_flag, 0)
        self.assertFalse(hasattr(r.select[0].filter, 'ignored_option'))

    def test_build_group_obj(self):

        q_filter_defs = [
            {
                'name': 'Fake Sensor',
                'filter': {
                    'operator': 'regexmatch',
                    'not_flag': 0,
                    'value': '.*'
                },
                'sensor_obj': self.sensor_obj_no_params
            }
        ]

        q_option_defs = {
            'all_values_flag': 0,
            'ignore_case_flag': 1,
            'max_age_seconds': '3600',
            'value_type': 'string',
            'all_times_flag': 0,
            'and_flag': 1,
            'ignored_option': 'tt',
        }

        kwargs = {
            'q_filter_defs': q_filter_defs,
            'q_option_defs': q_option_defs,
        }

        r = utils.build_group_obj(**kwargs)

        self.assertIsInstance(r, taniumpy.Group)
        self.assertIsInstance(r.filters, taniumpy.FilterList)
        self.assertEqual(len(r.filters), 1)
        self.assertIsInstance(r.filters[0], taniumpy.Filter)
        self.assertEqual(
            r.filters[0].sensor.hash, self.sensor_obj_no_params.hash)
        self.assertEqual(r.filters[0].operator, 'RegexMatch')
        self.assertEqual(r.filters[0].not_flag, 0)
        self.assertEqual(r.filters[0].value, '.*')
        self.assertEqual(r.filters[0].all_values_flag, 0)
        self.assertEqual(r.filters[0].ignore_case_flag, 1)
        self.assertEqual(r.filters[0].max_age_seconds, 3600)
        self.assertEqual(r.filters[0].value_type, 'String')
        self.assertEqual(r.filters[0].all_times_flag, 0)
        self.assertFalse(hasattr(r.filters[0], 'ignored_option'))

    def test_build_manual_q(self):
        r = utils.build_manual_q(taniumpy.SelectList(), taniumpy.Group())
        self.assertIsInstance(r, taniumpy.Question)
        self.assertIsInstance(r.group, taniumpy.Group)
        self.assertIsInstance(r.selects, taniumpy.SelectList)

    def test_build_selectlist_obj_invalid_filter(self):

        sensor_defs = [
            {
                'name': 'Fake Sensor',
                'filter': {
                    'operator': 'egexMatch',
                    'value': '.*'
                },
                'sensor_obj': self.sensor_obj_no_params
            }
        ]

        kwargs = {'sensor_defs': sensor_defs}
        e = "Invalid filter.*"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            utils.build_selectlist_obj(**kwargs)

    def test_build_selectlist_obj_missing_value(self):
        sensor_defs = [
            {
                'name': 'Fake Sensor',
                'filter': {
                    'operator': 'RegexMatch',
                },
                'sensor_obj': self.sensor_obj_no_params
            }
        ]

        kwargs = {'sensor_defs': sensor_defs}
        e = ".*requires a 'value' key!"
        with self.assertRaisesRegexp(DefinitionParserError, e):
            utils.build_selectlist_obj(**kwargs)


class TestGenericUtils(unittest.TestCase):
    def test_is_list(self):
        self.assertTrue(utils.is_list([]))

    def test_is_not_list(self):
        self.assertFalse(utils.is_list(''))

    def test_is_str(self):
        self.assertTrue(utils.is_str(''))

    def test_is_not_str(self):
        self.assertFalse(utils.is_str([]))

    def test_is_dict(self):
        self.assertTrue(utils.is_dict({}))

    def test_is_not_dict(self):
        self.assertFalse(utils.is_dict([]))

    def test_is_num(self):
        self.assertTrue(utils.is_num(2))

    def test_is_not_num(self):
        self.assertFalse(utils.is_num({}))

    def test_version_lower(self):
        self.assertTrue(utils.version_check('0.0.0'))

    def test_get_now(self):
        self.assertTrue(utils.get_now())

    def test_jsonify(self):
        exp = '{\n  "x": "d"\n}'
        self.assertEquals(utils.jsonify({'x': 'd'}), exp)

    def test_invalid_port(self):
        self.assertFalse(utils.port_check('localhost', 1, 0))

    def test_version_higher(self):
        req_ver = "100.100.100"
        e = (
            "Script and API Version mismatch.*version {}, required {}"
        ).format(pytan.__version__, req_ver)
        with self.assertRaisesRegexp(Exception, e):
            utils.version_check(req_ver)

    def test_empty_obj(self):
        obj = taniumpy.SensorList()
        self.assertTrue(utils.empty_obj(obj))
        self.assertTrue(utils.empty_obj(''))

    def test_ask_kwargs(self):
        kwargs = {'timeout': 2, 'other': 4, 'row_start': 5}
        ask_kwargs = utils.get_ask_kwargs(**kwargs)
        self.assertEqual(ask_kwargs, {'timeout': 2})

    def test_req_kwargs(self):
        kwargs = {'timeout': 2, 'other': 4, 'row_start': 5}
        req_kwargs = utils.get_req_kwargs(**kwargs)
        self.assertEqual(req_kwargs, {'row_start': 5})

    def test_get_q_obj_map(self):
        qtype = 'saved'
        self.assertEqual(utils.get_q_obj_map(qtype), {'handler': 'ask_saved'})

        qtype = 'manual'
        self.assertEqual(utils.get_q_obj_map(qtype), {'handler': 'ask_manual'})

        qtype = 'manual_human'
        self.assertEqual(
            utils.get_q_obj_map(qtype), {'handler': 'ask_manual_human'})

        qtype = ''
        e = (
            ".*not a valid question type, must be one of.*"
        )
        with self.assertRaisesRegexp(HandlerError, e):
            utils.get_q_obj_map(qtype)

        qtype = 'invalid'
        e = (
            ".*not a valid question type, must be one of.*"
        )
        with self.assertRaisesRegexp(HandlerError, e):
            utils.get_q_obj_map(qtype)

    def test_get_obj_map(self):
        obj = 'sensor'
        exp = {
            'single': 'Sensor',
            'multi': 'SensorList',
            'all': 'SensorList',
            'search': ['id', 'name', 'hash'],
            'manual': False,
            'delete': True,
            'create_json': True,
        }
        self.assertEqual(utils.get_obj_map(obj), exp)

        obj = 'invalid'
        e = (
            ".*not a valid object to get, must be one of.*"
        )
        with self.assertRaisesRegexp(HandlerError, e):
            utils.get_obj_map(obj)


class TestDeserializeBadXML(unittest.TestCase):
    def test_bad_chars_basetype(self):
        a = open(os.path.join(my_dir, 'bad_chars_basetype.xml'), 'rb+').read()
        b = pytan.taniumpy.session.xml_fix(a)
        c = pytan.taniumpy.BaseType.fromSOAPBody(b)
        self.assertTrue(c)
        self.assertIsInstance(c, taniumpy.SystemStatusList)

    def test_bad_chars_resultset(self):
        a = open(os.path.join(my_dir, 'bad_chars_resultset.xml'), 'rb+').read()
        b = pytan.taniumpy.session.xml_fix(a)
        el = pytan.taniumpy.session.ET.fromstring(b)
        cdata = el.find('.//ResultXML')
        rd = pytan.taniumpy.session.ET.fromstring(pytan.taniumpy.session.xml_fix(cdata.text))
        c = pytan.taniumpy.ResultSet.fromSOAPElement(rd)
        self.assertTrue(c)
        self.assertIsInstance(c, taniumpy.ResultSet)


if __name__ == "__main__":
    unittest.main(
        verbosity=TESTVERBOSITY,
        failfast=FAILFAST,
        catchbreak=CATCHBREAK)
