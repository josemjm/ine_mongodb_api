#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

import pymongo
import configparser


def db_parameters():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    host = config.get('DATABASE', 'host')
    port = config.get('DATABASE', 'port')
    username = config.get('DATABASE', 'user')
    password = config.get('DATABASE', 'password')
    db_name = config.get('DATABASE', 'db')

    return host, port, username, password, db_name


def conn_mongodb():
    # Get the database parameters
    host, port, username, password, db_name = db_parameters()

    # Set the MongoDB configuration
    client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/")
    db = client[db_name]

    return client, db


def create_unique_compound_index(database: pymongo.database.Database, collection_name: str, fields: list, index_name: str) -> str:
    """
    COMPOUND INDEX
        A single index structure holds references to multiple fields [1] within a collection's documents
        Sort order: pymongo.ASCENDING (1) or pymongo.DESCENDING (-1)
        Unique Compound Index: enforce uniqueness on the combination of the index key values
    """
    # Create unique Compound Index
    collection = database[collection_name]

    # Create a list with index fields
    idx_fields = []
    for field in fields:
        idx_tuple = (field, pymongo.ASCENDING)
        idx_fields.append(idx_tuple)

    # Create an unique index for index fields
    idx = collection.create_index(idx_fields,
                                  name=index_name,
                                  unique=True)

    # Get indexes
    # collection.index_information()

    # Drop index
    # collection.drop_index(index_name)

    return idx


def insert_data(payload: list, collection_name: str, database: pymongo.database.Database):
    # Insert new data based on UNIQUE ID
    collection = database[collection_name]
    try:
        result = collection.insert_many(payload, ordered=False)
    except pymongo.errors.BulkWriteError as e:
        print(str(e))

    return
