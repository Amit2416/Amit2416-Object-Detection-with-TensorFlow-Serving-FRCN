from typing import List
from pymongo import MongoClient

from counter.domain.models import ObjectCount
from counter.domain.ports import ObjectCountRepo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from counter.adapters.postgressql_model import Base, ObjectCountEntity


class CountInMemoryRepo(ObjectCountRepo):

    def __init__(self):
        self.store = dict()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        if object_classes is None:
            return list(self.store.values())

        return [self.store.get(object_class) for object_class in object_classes]

    def update_values(self, new_values: List[ObjectCount]):
        for new_object_count in new_values:
            key = new_object_count.object_class
            try:
                stored_object_count = self.store[key]
                self.store[key] = ObjectCount(key, stored_object_count.count + new_object_count.count)
            except KeyError:
                self.store[key] = ObjectCount(key, new_object_count.count)


class CountMongoDBRepo(ObjectCountRepo):

    def __init__(self, host, port, database):
        self.__host = host
        self.__port = port
        self.__database = database

    def __get_counter_col(self):
        client = MongoClient(self.__host, self.__port)
        db = client[self.__database]
        counter_col = db.counter
        return counter_col

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        counter_col = self.__get_counter_col()
        query = {"object_class": {"$in": object_classes}} if object_classes else None
        counters = counter_col.find(query)
        object_counts = []
        for counter in counters:
            object_counts.append(ObjectCount(counter['object_class'], counter['count']))
        return object_counts

    def update_values(self, new_values: List[ObjectCount]):
        counter_col = self.__get_counter_col()
        for value in new_values:
            counter_col.update_one({'object_class': value.object_class}, {'$inc': {'count': value.count}}, upsert=True)


class CountPostgreSQLRepo(ObjectCountRepo):
    def __init__(self, host, port, database):
        self.engine = create_engine(f"postgresql://{host}:{port}/{database}")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        query = self.session.query(ObjectCountEntity).filter(
            ObjectCountEntity.object_class.in_(object_classes)) if object_classes else self.session.query(
            ObjectCountEntity)
        return [ObjectCount(row.object_class, row.count) for row in query]

    def update_values(self, new_values: List[ObjectCount]):
        for new_object_count in new_values:
            existing_record = self.session.query(ObjectCountEntity).filter_by(object_class=new_object_count.object_class).first()
            if existing_record:
                existing_record.count += new_object_count.count
            else:
                new_record = ObjectCountEntity(object_class=new_object_count.object_class, count=new_object_count.count)
                self.session.add(new_record)
        self.session.commit()
