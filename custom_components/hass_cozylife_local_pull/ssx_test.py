import json

def get_local_get_pid_list() -> str:
    file0 = open('api-us.doiting.comapidevice_productmodellangen20230525.json', "r")
    content = file0.read()
    # print(type(content))  # <class 'str'>
    # print(content)
    file0.close()
    return json.loads(content)
