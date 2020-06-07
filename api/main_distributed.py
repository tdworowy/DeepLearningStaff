from rest_api_distributed import read_config, get_app

if __name__ == '__main__':
    config = read_config()
    get_app().run(host=config.get('flask_host'), port=config.get('port'), threaded=False, debug=True)