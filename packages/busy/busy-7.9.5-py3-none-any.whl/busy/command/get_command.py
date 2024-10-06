from busy.command import BusyCommand, CollectionCommand, IntegrationCommand

from wizlib.parser import WizParser


class GetCommand(CollectionCommand, IntegrationCommand):
    """Gets a value from an integration"""

    name = 'get'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('integration')
        parser.add_argument('key')

    @BusyCommand.wrap
    def execute(self):
        return self.execute_integration()
