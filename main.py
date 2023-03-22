from tapi_yandex_market import YandexMarket


def get_region_id(name):
    region_response = client.geo_regions().get(params={'name': name})
    print(region_response.data)
    region_response_data = region_response.data
    region_id = None
    regions = region_response_data.get('regions', list())
    for r in regions:
        if r.get('name', None) == 'Москва':
            region_id = r.get('id', None)
    if region_id is None:
        raise Exception()
    return region_id


def fab_validator_intel(i=7, second=9700, suffix='k'):
    suffix = suffix.upper()

    def validate_model_intel(model):
        name = model.get('name', "").upper()
        if f"I{i}" not in name:
            return False
        if f"{second}{suffix} " not in name:
            return False
        for ban_word in ('КОМПЬЮТЕР', 'СИСТЕМНЫЙ', 'БЛОК'):
            if ban_word in name:
                return False
        return True

    return validate_model_intel


def get_models(with_name, pages_max_count, by_validation):
    validated_models = []
    for page in range(1, pages_max_count + 1):
        models_response = client.models().get(
            params={'query': with_name,
                    'regionId': region_id,
                    'page': page,
                    'pageSize': 100})
        models_response_data = models_response.data
        models = models_response_data \
            .get('models', dict()) \
            .get('models', list())
        new_validated_models = list(filter(by_validation, models))
        print(new_validated_models)
        print()
        validated_models.append(new_validated_models)


OAUTH_TOKEN = "y0_AgAAAAAOwmjOAAkb5AAAAADbt1VxCdTy_1eVQDWpw-20RAxKuNbJJvs"
OAUTH_CLIENT_ID = "84e77c8cfb684f8a9f2a5983a51f171c"
client = YandexMarket(
    # https://yandex.ru/dev/market/partner/doc/dg/concepts/authorization.html
    oauth_token=OAUTH_TOKEN,
    oauth_client_id=OAUTH_CLIENT_ID,
    # Will retry the request if the request limit is reached.
    retry_if_exceeded_requests_limit=True,
)
result = client.campaigns().get()
# Raw data.
print(result.data)
print(*dir(client), sep='\n')

region_id = get_region_id('Москва')
print(region_id)
params = {}
get_models('i7 12700k', 10, fab_validator_intel(7, 12700, 'f'))
models_info_response = client.model_offers(modelId=232387065).get(
    params={'regionId': region_id})
print(models_info_response.data)
