import configparser
import json
import xml.etree.ElementTree as ET
import yaml

class ConfigParser:
    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type.lower()
        self.config_data = self.parse()

    def parse(self):
        if self.file_type == 'ini':
            return self.parse_ini()
        elif self.file_type == 'json':
            return self.parse_json()
        elif self.file_type == 'xml':
            return self.parse_xml()
        elif self.file_type == 'yaml':
            return self.parse_yaml()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def parse_ini(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)
        return config

    def parse_json(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def parse_xml(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return self.xml_to_dict(root)

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

    def parse_yaml(self):
        with open(self.file_path, 'r') as f:
            return yaml.safe_load(f)

    def update(self, key:str, value):
        """修改配置文件中的值

        Args:
            key (str): 要修改的配置项的键,对于嵌套的配置项,使用点(.)分隔每一级的键。
            value (Any): 要设置的新值。

        Raises:
            ValueError: 不支持的配置
        """
        if self.file_type == 'ini':
            self.update_ini(key, value)
        elif self.file_type == 'json':
            self.update_json(key, value)
        elif self.file_type == 'xml':
            self.update_xml(key, value)
        elif self.file_type == 'yaml':
            self.update_yaml(key, value)
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def update_ini(self, key, value):
        section, option = key.split('.')
        self.config_data.set(section, option, str(value))
        with open(self.file_path, 'w') as f:
            self.config_data.write(f)

    def update_json(self, key, value):
        keys = key.split('.')
        data = self.config_data
        for k in keys[:-1]:
            data = data[k]
        data[keys[-1]] = value
        with open(self.file_path, 'w') as f:
            json.dump(self.config_data, f, indent=4)

    def update_xml(self, key, value):
        # TODO: Implement XML update
        pass

    def update_yaml(self, key, value):
        keys = key.split('.')
        data = self.config_data
        for k in keys[:-1]:
            data = data[k]
        data[keys[-1]] = value
        with open(self.file_path, 'w') as f:
            yaml.dump(self.config_data, f)
