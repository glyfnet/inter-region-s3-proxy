import os, boto3, botocore, fastapi, bmemcached
from typing import Optional, List

ORIGIN_BUCKET = 'usgs-landsat'
LOCAL_BUCKET = 'grr-sydney.amazon.com'
LOCAL_PREFIX = 'datacube'
MEMECACHED_ENDPOINT = 'http://landsat.gwbbqw.cfg.apse2.cache.amazonaws.com:11211'

app = fastapi.FastAPI()
s3 = boto3.client('s3')
s3_object_waiter = s3.get_waiter('object_exists')
memcached = bmemcached.Client(MEMECACHED_ENDPOINT)

@app.get('/healthcheck')
async def healthcheck():
    return {'message': 'All good.'}
    
# to get local object, without copying from origin
@app.get('/local/{key:path}') 
async def get_object_local(key: str):
    response = s3.get_object(Bucket=LOCAL_BUCKET, Key=f'{LOCAL_PREFIX}/{key}', RequestPayer='requester')
    return fastapi.responses.StreamingResponse(response['Body'].iter_chunks())

# to list local objects          
@app.get('/local')   
async def list_v2_local(prefix: Optional[str]=None):
    return s3.list_objects_v2(Bucket=LOCAL_BUCKET, Prefix=f'{LOCAL_PREFIX}/{prefix}')
    
# to get origin object directly
@app.get('/origin/{key:path}') 
async def get_object_origin(key: str):
    response = s3.get_object(Bucket=ORIGIN_BUCKET, Key=key, RequestPayer='requester')
    return fastapi.responses.StreamingResponse(response['Body'].iter_chunks())
    
# default get on root with key will get the object from local, and copy it from origin if needed       
@app.get('/{key:path}')
async def get_object(key: str):
    local_object = {'Bucket': LOCAL_BUCKET, 'Key': f'{LOCAL_PREFIX}/{key}'}
        
    try:
        response = s3.head_object(**local_object)
        
    except botocore.exceptions.ClientError:
        print('copying object')
        response = s3.copy_object(**local_object, CopySource=f'/{ORIGIN_BUCKET}/{key}', RequestPayer='requester')
        print('waiting for copy object')
        s3_object_waiter.wait(**local_object)
    
    print('get object')
    response = s3.get_object(**local_object)
    print('streaming response')
    return fastapi.responses.StreamingResponse(response['Body'].iter_chunks())
    
# default get on root will list objects from origin 
@app.get('/')
async def list_v2(prefix: Optional[str]=None):
    return s3.list_objects_v2(Bucket=ORIGIN_BUCKET, Prefix=prefix, RequestPayer='requester')

@app.get('/cache/{key:path}') 
async def get_object_cache(key: str):
    return memcached.get('key', 'value')
