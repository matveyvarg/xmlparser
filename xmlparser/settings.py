import os
DB_HOST = os.getenv('DB_HOST', 'file.db')
PAGE_SIZE = int(os.getenv('PAGE_SIZE', '10'))
HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', '8080')
DEBUG = True
FIELDS = [('ProgramInformation', ('programId',)), ('Title',), ('InstanceMetadataId',), ('StartOfAvailability',), ('EndOfAvailability'), ('Title',('episodeTitle',)), ('Genre',),('OtherIdentifier', ('type', 'value')),('GroupId',)]