# AnhaltAI Commons Minio
Provides functionality for data management between Python code and Minio stores, 
from basic operations on Minio clients, buckets, files, and directories to more complex 
operations such as copying and migrating directory-based datasets.

The package provides extended functionality for the usage to the minio package.

## structure
The provided functions are divided into several levels.

### adapters
Adapters provide functions to enable data operations between Minio and other data stores

#### nextcloud.py
Contains a subclass of a nextcloud client to provide functions to execute copy 
operations for files and directories between Minio and Nextcloud

### io_utils.py
Provides functions to fulfill CRUD operations for files and directories

### bucket_utils.py
Allows operations on buckets by the provided functions.

### client_utils.py
Allows operations on clients by the provided functions.

### tests
- the package is tested by automated testa to ensure functionality
- Install ``pytest`` and ``pytest-minio-mock``.
- The config pytest.ini contains further settings as explained here: 
https://docs.pytest.org/en/7.1.x/reference/customize.html
- Run
````shell
pytest tests
````