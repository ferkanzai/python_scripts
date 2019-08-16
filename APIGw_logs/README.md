# Scripts to for with API Gateway execution logs from CloudWatch

Those logs come with each stream inside a folder and zipped. 
Use unzip_all.py to extract all logs to a different folder.
Use read_API_logs.py to check for ogs with a 200 response and logs with a 403 response with a later execution time.