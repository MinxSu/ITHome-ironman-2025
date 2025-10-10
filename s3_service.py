import boto3

class S3Service:
   
   def read_s3_file_local(self, bucket_name: str, object_key: str, encoding: str = "utf-8"):
    session = boto3.Session(profile_name="dev-s3-ironman2025")
    client = session.client("s3")
    return self.__read_s3_file(client, bucket_name, object_key, encoding)

   def read_s3_file(self, bucket_name: str, object_key: str, encoding: str = "utf-8"):
    client = boto3.client("s3")
    return self.__read_s3_file(client, bucket_name, object_key, encoding)

   def __read_s3_file(self, client, bucket_name: str, object_key: str, encoding: str ) -> str:
    """
    讀取 AWS S3 上的檔案並回傳內容
    :param bucket_name: S3 bucket 名稱
    :param object_key: 檔案路徑
    :param encoding: 文字編碼，預設 utf-8
    :return: 檔案內容（字串）
    """
    
    try:
        response = client.get_object(Bucket=bucket_name, Key=object_key)
        content = response["Body"].read().decode(encoding)
        return content
    except Exception as e:
        print(f"讀取 S3 檔案時發生錯誤: {e}")
        return ""