import json
import yaml
import os
from jsonschema import validate
from urllib.parse import urlparse
from exceptions import ValidationException

#  code as newspaper
# типизация mypy
# precommit hook git on linters
# conventional comments
class ContractValidator(object):
    def __init__(self) -> None:
        pass

    def validate_by_schema(self, contract_file, schema_file):
        contract = self._read_file(contract_file)
        schema = self._read_file(schema_file)
        validate(instance=contract, schema=schema)

    def validate_by_spec(self, contract_file, spec_file):
        contract = self._read_file(contract_file)
        spec = self._read_file(spec_file)
        # TODO: how to get provider from spec
        # if contract['provider'] != 
        for index, interaction in enumerate(contract['http_interactions']):
            # TODO: proper exceptions
            # TODO: add index to exception
            uri = interaction['request']['uri']
            uri_parsed = urlparse(uri)
            path = uri_parsed.path
            if path not in spec['paths']:
                raise ValidationException(f'Given inappropriate path "{path}" in interaction[{index}]')
            method = interaction['request']['method'].lower()
            if method not in list(map(lambda x: x.lower(), spec['paths'][path])):
                raise ValidationException(f'Path "{path}" does not support method "{method}"')
            # TODO: request payload
            status_code = interaction['response']['status']['code']
            if status_code not in spec['paths'][path][method]['responses']:
                raise ValidationException(f'Requested path "{path}" does not support  method "{method}"')
            contract_payload = interaction['response']['body']['string']
            # TODO: encoding = 
            content_type = interaction['response']['headers']['content-type']
            if contract_payload:
                if content_type not in spec['paths'][path][method]['responses'][status_code]['content']:
                    # TODO
                    raise ValidationException()
            else:
                # TODO
                is_contains_empty_response = False
                for content in spec['paths'][path][method]['responses'][status_code]['content']:
                    if not content:
                        is_contains_empty_response = True
                if not is_contains_empty_response:
                    raise ValidationException()

                    
    def _read_file(self, file_name):
        with open(file_name) as stream:
            if os.path.splitext(file_name)[1] == '.yaml':
                file = yaml.safe_load(stream)
            elif os.path.splitext(file_name)[1] == '.json':
                file = json.load(stream)
            else:
                raise ValidationException(f'File "{file_name}" has inappropriate file extension') 
            return file


def main():
    validator = ContractValidator()
    contract_file = './contract.json'
    contract_schema = './contract_schema.json'
    spec_file = './spec.json'
    validator.validate_by_schema(contract_file, contract_schema)
    validator.validate_by_spec(contract_file, spec_file)


if __name__ == "__main__":
    main()