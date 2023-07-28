import requests
import json

if __name__ == "__main__":
    headers = {'Content-Type': 'application/json'}
    data = {"jsonrpc": "2.0"}
    db = "test"
    login = "admin"
    password = "admin"
    base_url = 'http://localhost:9014'
    print("BaseURL %s" % str(base_url))

    print("#################################### /web/session/authenticate #######################################")
    url_path = '/web/session/authenticate'
    params = {"db": db, "login": login, "password": password}
    print("Login details", str(params))
    data['params'] = params
    data_json = json.dumps(data)
    req = requests.post('{}/web/session/authenticate'.format(base_url), data=data_json, headers=headers)
    cookie_dictionary = req.cookies.get_dict()
    if "session_id" in cookie_dictionary:
        session_str = "session_id = " + str(cookie_dictionary['session_id'])
        headers["cookie"] = session_str
    # print("/web/session/authenticate response json", req.content.decode('utf-8'))
    print("URL Path: %s" % url_path)
    print("headers json", headers)

    print("####################################/api/v1/trip/detail #####################################")
    # headers["cookie"] = "session_id = 49933546b9f59228d8026117e39c1a5d5cbd906e"
    url_path = '/api/v1/trip/detail'
    params = {
        "trip_id": 1
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("####################################/api/v1/trips #####################################")
    # headers["cookie"] = "session_id = 49933546b9f59228d8026117e39c1a5d5cbd906e"
    url_path = '/api/v1/trips'
    params = {
        # "user_id": 1
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("####################################/api/v1/leads/activity #####################################")
    # headers["cookie"] = "session_id = 49933546b9f59228d8026117e39c1a5d5cbd906e"
    url_path = '/api/v1/leads/activity'
    params = {
        "trip_id": 1
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("####################################/api/v1/leads/detail #####################################")
    # headers["cookie"] = "session_id = 49933546b9f59228d8026117e39c1a5d5cbd906e"
    url_path = '/api/v1/leads/detail'
    params = {
        "trip_id": 2
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    # print("####################################/api/v1/trip/start #####################################")
    # # headers["cookie"] = "session_id = 49933546b9f59228d8026117e39c1a5d5cbd906e"
    # url_path = '/api/v1/trip/start'
    # params = {
    #     "trip_id": 1
    # }
    # data['params'] = params
    # data_json = json.dumps(data)
    # print("URL Path: %s" % url_path)
    # print("Input Json: %s" % data)
    #
    # print("####################################/api/v1/trip/complete #####################################")
    # # headers["cookie"] = "session_id = 49933546b9f59228d8026117e39c1a5d5cbd906e"
    # url_path = '/api/v1/trip/complete'
    # params = {
    #     "trip_id": 1
    # }
    # data['params'] = params
    # data_json = json.dumps(data)
    # print("URL Path: %s" % url_path)
    # print("Input Json: %s" % data)
    #
    # print("####################################/api/v1/trip/cancel #####################################")
    # url_path = '/api/v1/trip/cancel'
    # params = {
    #     "trip_id": 1
    # }
    # data['params'] = params
    # data_json = json.dumps(data)
    # print("URL Path: %s" % url_path)
    # print("Input Json: %s" % data)
    print("####################################/api/v1/trip/meet/start #####################################")
    url_path = '/api/v1/trip/meet/start'
    params = {
        "trip_id": 1,
        "customer_id": 1
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("####################################/api/v1/trip/meet/complete #####################################")
    url_path = '/api/v1/trip/meet/complete'
    params = {
        "trip_id": 1,
        "customer_id": 1
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("####################################/api/v1/trip/lead/location #####################################")
    url_path = '/api/v1/trip/lead/location'
    params = {
        "trip_id": 1,
        "customer_id": 1,
        "latitude": 12.122,
        "longitude": 12.122
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("####################################/api/v1/trip/meet/reached #####################################")
    url_path = '/api/v1/trip/meet/reached'
    params = {
        "trip_id": 1,
        "customer_id": 1,
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("####################################/api/v1/trip/meet/cancel #####################################")
    url_path = '/api/v1/trip/meet/cancel'
    params = {
        "trip_id": 1,
        "customer_id": 1,
    }
    data['params'] = params
    data_json = json.dumps(data)
    print("URL Path: %s" % url_path)
    print("Input Json: %s" % data)

    print("#########################################################################")
    req = requests.post('{}{}'.format(base_url, url_path), data=data_json, headers=headers)
    print("%s response json: %s" % (str(url_path), str(req.content.decode('utf-8'))))

