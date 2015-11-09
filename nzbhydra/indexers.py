from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library

from peewee import fn

standard_library.install_aliases()
from builtins import *
import logging
from nzbhydra import config, database
from nzbhydra.database import Indexer
from nzbhydra.searchmodules import newznab, womble, nzbclub, nzbindex, binsearch

logger = logging.getLogger('root')

configured_indexers = []



def init_indexer_table_entry(indexer_name):
    try:
        Indexer.get(fn.lower(Indexer.name) == indexer_name.lower())
    except Indexer.DoesNotExist as e:
        logger.info("Unable to find indexer with name %s in database. Will add it" % indexer_name)
        Indexer().create(name=indexer_name)

# Load from config and initialize all configured indexers using the loaded modules
def read_indexers_from_config():
    database.db.connect()
    global configured_indexers
    configured_indexers = []

    if config.indexerSettings.binsearch.enabled.get():
        instance = binsearch.get_instance(config.indexerSettings.binsearch)
        configured_indexers.append(instance)
        init_indexer_table_entry(instance.name)
        logger.info("Loaded indexer %s" % instance.name)
        
    if config.indexerSettings.nzbindex.enabled.get():
        instance = nzbindex.get_instance(config.indexerSettings.nzbindex)
        configured_indexers.append(instance)
        init_indexer_table_entry(instance.name)
        logger.info("Loaded indexer %s" % instance.name)
        
    if config.indexerSettings.nzbclub.enabled.get():
        instance = nzbclub.get_instance(config.indexerSettings.nzbclub)
        configured_indexers.append(instance)
        init_indexer_table_entry(instance.name)
        logger.info("Loaded indexer %s" % instance.name)
        
    if config.indexerSettings.womble.enabled.get():
        instance = womble.get_instance(config.indexerSettings.womble)
        configured_indexers.append(instance)
        init_indexer_table_entry(instance.name)
        logger.info("Loaded indexer %s" % instance.name)
        
    for i in range(1, 7):
        newznabsetting = config.get_newznab_setting_by_id(i)
        if newznabsetting.enabled.get():
            instance = newznab.get_instance(newznabsetting)
            configured_indexers.append(instance)
            init_indexer_table_entry(instance.name)
            logger.info("Loaded indexer %s" % instance.name)
                  
    database.db.close()            
    return configured_indexers


