from pymongo import MongoClient
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import log as LOG

class MongoDBHandler:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='EmoDB'):
        # 连接到MongoDB服务器
        self.client = MongoClient(uri)
        # 选择数据库
        self.db = self.client[db_name]
        LOG.log_message("Connected to MongoDB", level='info')

    def insert_document(self, document, collection_name='images'):
        """插入单个文档"""
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        LOG.log_message(f"Document inserted with ID: {result.inserted_id}", level='info')
        return result.inserted_id

    def find_document(self, query, collection_name='images'):
        """查找单个文档"""
        collection = self.db[collection_name]
        document = collection.find_one(query)
        LOG.log_message(f"Document found: {document}", level='info')
        return document

    def find_all_documents(self, query={}, collection_name='images'):
        """查找所有文档"""
        collection = self.db[collection_name]
        documents = list(collection.find(query))
        LOG.log_message(f"Found {len(documents)} documents", level='info')
        return documents

    def update_document(self, query, update_data, collection_name='images'):
        """更新单个文档"""
        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': update_data})
        LOG.log_message(f"Document updated: {result.modified_count}", level='info')
        return result.modified_count

    def delete_document(self, query, collection_name='images'):
        """删除单个文档"""
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        LOG.log_message(f"Document deleted: {result.deleted_count}", level='info')
        return result.deleted_count

    def close(self):
        """关闭数据库连接"""
        LOG.log_message("Closing MongoDB connection", level='info')
        self.client.close()


if __name__ == '__main__':
    # 测试MongoDBHandler类
    db_handler = MongoDBHandler()