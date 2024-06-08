import configparser
import json
import xml.etree.ElementTree as ET
import yaml

class ConfigParser:
    def __init__(self, config_source, data_type, from_file=True):
        self.config_source = config_source
        self.data_type = data_type.lower()
        self.from_file = from_file
        self.config_data = self.parse()

    def parse(self):
        if self.from_file:
            return self.parse_from_file()
        else:
            return self.parse_from_string()

    def parse_from_file(self):
        if self.data_type == 'ini':
            return self.parse_ini_file()
        elif self.data_type == 'json':
            return self.parse_json_file()
        elif self.data_type == 'xml':
            return self.parse_xml_file()
        elif self.data_type == 'yaml':
            return self.parse_yaml_file()
        else:
            raise ValueError(f"Unsupported file type: {self.data_type}")

    def parse_from_string(self):
        if self.data_type == 'ini':
            return self.parse_ini_string()
        elif self.data_type == 'json':
            return self.parse_json_string()
        elif self.data_type == 'xml':
            return self.parse_xml_string()
        elif self.data_type == 'yaml':
            return self.parse_yaml_string()
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")

    def parse_ini_file(self):
        config = configparser.ConfigParser()
        config.read(self.config_source)
        return config

    def parse_json_file(self):
        with open(self.config_source, 'r') as f:
            return json.load(f)

    def parse_xml_file(self):
        tree = ET.parse(self.config_source)
        root = tree.getroot()
        return self.xml_to_dict(root)

    def parse_yaml_file(self):
        with open(self.config_source, 'r') as f:
            return yaml.safe_load(f)

    def parse_ini_string(self):
        config = configparser.ConfigParser()
        config.read_string(self.config_source)
        return config

    def parse_json_string(self):
        return json.loads(self.config_source)

    def parse_xml_string(self):
        root = ET.fromstring(self.config_source)
        return self.xml_to_dict(root)

    def parse_yaml_string(self):
        return yaml.safe_load(self.config_source)

    def xml_to_dict(self, root):
        result = {}
        if root.text and root.text.strip():
            result['_text'] = root.text.strip()
        for child in root:
            if child.tag in result:
                if isinstance(result[child.tag], list):
                    result[child.tag].append(self.xml_to_dict(child))
                else:
                    result[child.tag] = [result[child.tag], self.xml_to_dict(child)]
            else:
                result[child.tag] = self.xml_to_dict(child)
        return result

    def update(self, key, value):
        if self.data_type == 'ini':
            self.update_ini(key, value)
        elif self.data_type == 'json':
            self.update_json(key, value)
        elif self.data_type == 'xml':
            self.update_xml(key, value)
        elif self.data_type == 'yaml':
            self.update_yaml(key, value)
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")

    def update_ini(self, key, value):
        section, option = key.split('.')
        self.config_data.set(section, option, str(value))

    def update_json(self, key, value):
        keys = key.split('.')
        data = self.config_data
        for k in keys[:-1]:
            data = data[k]
        data[keys[-1]] = value

    def update_xml(self, key, value):
        # TODO: Implement XML update
        pass

    def update_yaml(self, key, value):
        keys = key.split('.')
        data = self.config_data
        for k in keys[:-1]:
            data = data[k]
        data[keys[-1]] = value
