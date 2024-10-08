import yaml, json
from os.path import join, isfile
from pprint import pprint as pp

# Import apc and execute_pipeline from auto_reflection
from auto_reflection import apc, execute_pipeline


# Set verbose to True
apc.verbose = True
# auto_reflection/main.py

def main():
    if 1:  # mock
        py_pipeline_name = 'mocked_topics'

        yaml_pprompt_config = join('yaml_config', 'topics.yaml')

        title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
        if 1:
            mock_file = join('mock', 'blog_writer', 'topics.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file)  # Access apc to load mock data
    print(title, py_pipeline_name, yaml_pprompt_config)
    apc.title, apc.py_pipeline_name, apc.yaml_pprompt_config = title, py_pipeline_name, yaml_pprompt_config  
    topics = execute_pipeline(apc.title, apc.py_pipeline_name, apc.yaml_pprompt_config)
    pp(json.loads(topics))


