import configparser

config = configparser.ConfigParser()
config.read("config.ini")

settings: dict = {}

audio_settings: dict = {}
audio_settings.update({'Audio_DEBUG': config.get('Audio', 'Audio_DEBUG')})
audio_settings.update({'Input_FORMAT': config.get('Audio', 'Input_FORMAT')})
audio_settings.update({'Input_CHANNELS': config.get('Audio', 'Input_CHANNELS')})
audio_settings.update({'Input_RATE': config.get('Audio', 'Input_RATE')})
audio_settings.update({'Input_CHUNK': config.get('Audio', 'Input_CHUNK')})
audio_settings.update({'Threshold_MAIN': config.get('Audio', 'Threshold_MAIN')})
graphic_settings: dict = {}
graphic_settings.update({'GUI_DEBUG': config.get('GUI', 'GUI_DEBUG')})
graphic_settings.update({'GUI_TITLE': config.get('GUI', 'GUI_TITLE')})
graphic_settings.update({'GUI_GEOMETRY': config.get('GUI', 'GUI_GEOMETRY')})

settings.update({'Audio': audio_settings})
settings.update({'GUI': graphic_settings})
