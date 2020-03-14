from rest_api_standard import read_config, get_app

if __name__ == '__main__':
    config = read_config()
    get_app().run(host=config.get('host'), port=config.get('port'), threaded=False)