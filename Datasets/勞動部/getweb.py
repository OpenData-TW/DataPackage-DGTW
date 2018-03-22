if k['RES_FILETYPE'] == 'WEBSERVICES':
    response = requests.get(k['RES_URL']).json()
    fname = r_json['TITLE'] + '.' + k['RES_FILETYPE'].lower()
    with open(oid_path + '\\' + fname, "w", encoding='utf-8') as handle:
        json.dump(response.json(), handle, ensure_ascii=False, indent=4)
