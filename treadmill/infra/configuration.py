from jinja2 import Template

from treadmill.infra import SCRIPT_DIR


class Configuration:
    """Configure instances"""

    def __init__(self, setup_scripts=None):
        self.setup_scripts = setup_scripts or []

    def get_userdata(self):
        if not self.setup_scripts:
            return ''

        userdata = ''
        # Add initializer script
        self.setup_scripts.insert(0, {'name': 'init.sh'})
        for script in self.setup_scripts:
            with open(SCRIPT_DIR + script['name'], 'r') as data:
                template = Template(data.read())
                userdata += template.render(script.get('vars', {})) + '\n'
        return userdata
