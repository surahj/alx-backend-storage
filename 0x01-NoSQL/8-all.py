#!/usr/bin/env python3
"""
lists all documents in a collection
"""
import pymongo


def list_all(mongo_collection):
    """
    list all documents
    """
    if len(list(mongo_collection.find())) < 1:
        return []
    return list(mongo_collection.find())
