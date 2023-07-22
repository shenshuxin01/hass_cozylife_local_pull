import json

def get_local_get_pid_list():
    file0 = open('/config/custom_components/hass_cozylife_local_pull/api-us.doiting.comapidevice_productmodellangen20230525.json', "r")
    content = file0.read()
    # print(type(content))  # <class 'str'>
    # print(content)
    file0.close()
    return content

def write_local_get_pid_list(s):
    file0 = open('/config/custom_components/hass_cozylife_local_pull/api-us.doiting.comapidevice_productmodellangen20230525.json', "w")
    file0.write(json.dumps(s, indent=2, ensure_ascii=False))  # ensure_ascii=False可以消除json包含中文的乱码问题
    file0.close()
