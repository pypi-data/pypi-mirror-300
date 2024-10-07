from unittest.mock import MagicMock
from enum import Enum


class QueryTypes(Enum):
    SIMPLE_TABLE = 'SIMPLE_TABLE'
    FUNCTION = 'FUNCTION'
    SEARCH = 'SEARCH'


class MockMicroFetcher:
    def __init__(self, data_mapping=None):
        self.data_mapping = data_mapping or {}
        self.instances = []

    def __call__(self, service_name):
        instance = MockMicroFetcherInstance(service_name, self.data_mapping)
        self.instances.append(instance)
        return instance


class MockMicroFetcherInstance:
    def __init__(self, service_name, data_mapping):
        self.service_name = service_name
        self.data_mapping = data_mapping

        # Internal state variables
        self.base_data = None
        self.fields = []
        self.table_name = None
        self.column_name = None
        self.compair_operator = None
        self.column_values = None
        self.output_key = None
        self.lookup_key = None
        self.module_name = None
        self.function_params = None
        self.query_type = None
        self.search_list = None
        self.configs = None
        self.search_configs = None
        self._global_configs = None
        self.filter_args = None

    def join(self, base_data, output_key=None):
        self.base_data = base_data
        self.query_type = QueryTypes.SIMPLE_TABLE.value
        if output_key:
            output_key = output_key.split('as ')[1] if 'as ' in output_key else output_key
        self.output_key = self.service_name.lower() if not output_key else output_key
        return self

    def config(self, **configs):
        self.configs = configs
        return self

    def search_config(self, configs):
        self.search_configs = configs
        self._prepare_search_list()
        return self

    def _prepare_search_list(self):
        output = dict()
        for index, item in enumerate(self.base_data):
            for search_column in self.search_configs.get("search_priority"):
                sanitize = None
                if isinstance(search_column, dict):
                    search_column_name = search_column.get('key')
                    operator = search_column.get('operator') or "IN"
                    sanitize = search_column.get('sanitize')
                else:
                    search_column_name = search_column
                    operator = 'IN'

                value = item.get(search_column_name)
                if sanitize and isinstance(sanitize, list):
                    for _san in sanitize:
                        value = _san(value)

                if value:
                    if not output.get(search_column_name):
                        output[search_column_name] = dict(
                            search_key=search_column_name,
                            operator=operator,
                            inputs=dict()
                        )
                    if not output[search_column_name]['inputs'].get(value):
                        output[search_column_name]['inputs'][value] = dict(
                            indexes=[index],
                            search_value=value
                        )
                    else:
                        output[search_column_name]['inputs'][value]["indexes"].append(index)
                    break

        output = list(output.values())
        for item in output:
            item['inputs'] = list(item['inputs'].values())

        self.search_list = output

    def global_configs(self, **keywords):
        self._global_configs = keywords
        return self

    def feed_list(self, base_data, output_key=None):
        self.join(base_data, output_key)
        self.query_type = QueryTypes.SEARCH.value
        return self

    def select(self, *args):
        self.fields.extend(args)
        return self

    def filter(self, *args):
        self.filter_args = args
        # Extract lookup_key and column_name
        self.lookup_key = args[2]
        column_parts = args[0].split('.')
        if len(column_parts) == 2:
            self.table_name, self.column_name = column_parts
        else:
            self.column_name = column_parts[0]
        return self

    def with_params(self, **kwargs):
        self.function_params = kwargs
        return self

    def from_function(self, module_name):
        self.query_type = QueryTypes.FUNCTION.value
        self.module_name = module_name
        return self

    def fetch(self):
        if self.base_data is not None:
            # Merge data into base_data
            self._merge_data_into_base()
            return self.base_data
        else:
            # Return data assigned to variable
            return self._get_return_data()

    def execute(self):
        # Return data assigned to variable
        return self._get_return_data()

    def _get_return_data(self):
        # Use data_mapping to get data based on internal state
        key = (self.service_name, self.module_name)
        return self.data_mapping.get(key, None)

    def _get_lookup_value(self, item, lookup_key):
        """Helper method to get value from dict or object."""
        keys = lookup_key.split('.')

        if isinstance(item, dict):
            # Handle dict
            for key in keys:
                item = item.get(key, None)
                if item is None:
                    break
            return item
        else:
            # Handle object attributes
            lookup_value = getattr(item, keys[0], None)
            for key in keys[1:]:
                lookup_value = getattr(lookup_value, key, None)
                if lookup_value is None:
                    break
            return lookup_value

    def _set_value(self, item, key, value):
        """Helper method to set value in dict or object."""
        if isinstance(item, dict):
            # Handle dict
            item[key] = value
        else:
            # Handle object attributes
            setattr(item, key, value)

    def _merge_data(self, data, data_to_merge):
        if isinstance(data, list):
            for item in data:
                # Get lookup value using our helper method
                lookup_value = self._get_lookup_value(item, self.lookup_key)

                # Match and set the value
                for data_item in data_to_merge:
                    if str(data_item.get(self.column_name)) == str(lookup_value):
                        self._set_value(item, self.output_key, data_item)
                        break
        elif isinstance(data, dict):
            # Handle the case where data itself is a dict
            lookup_value = self._get_lookup_value(data, self.lookup_key)
            for data_item in data_to_merge:
                if str(data_item.get(self.column_name)) == str(lookup_value):
                    self._set_value(data, self.output_key, data_item)
                    break

    def _merge_data_into_base(self):
        # Use data_mapping to get data to merge
        key = (self.service_name, self.output_key)
        data_to_merge = self.data_mapping.get(key, [])
        # Now merge data_to_merge into base_data
        if not data_to_merge:
            return

        # Check if base_data is an instance of flask_sqlalchemy.Pagination
        try:
            from flask_sqlalchemy import Pagination
        except ImportError:
            Pagination = None

        if Pagination and isinstance(self.base_data, Pagination):
            data = self.base_data.items
        else:
            data = self.base_data

        self._merge_data(data, data_to_merge)

    def __getattr__(self, item):
        # Return self for any undefined methods to support method chaining
        return self
