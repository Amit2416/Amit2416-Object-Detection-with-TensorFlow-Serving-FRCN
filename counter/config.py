import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects
from counter.adapters.count_repo import CountPostgreSQLRepo


def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


#def prod_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    mongo_host = os.environ.get('MONGO_HOST', 'localhost')
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))


def prod_count_action(database_type: str) -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)

    if database_type == 'mongodb':
        mongo_host = os.environ.get('MONGO_HOST', 'localhost')
        mongo_port = os.environ.get('MONGO_PORT', 27017)
        mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
        return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                    CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))
    elif database_type == 'postgresql':
        postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
        postgres_password = os.environ.get('POSTGRES_PASSWORD', 'password')
        postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
        postgres_port = os.environ.get('POSTGRES_PORT', 5432)
        postgres_db = os.environ.get('POSTGRES_DB', 'prod_counter')

        db_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                    CountPostgreSQLRepo(db_url))
    else:
        raise ValueError("Invalid database type. Supported types are 'mongodb' and 'postgresql'")


#def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()

def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    database_type = os.environ.get('DATABASE_TYPE', 'mongodb')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn](database_type)
