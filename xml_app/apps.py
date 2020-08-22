from django.apps import AppConfig


class XmlAppConfig(AppConfig):
    name = 'xml_app'

    def ready(self):
        from .tasks import checkExistingFiles
        print('app ready')
        checkExistingFiles.delay()
