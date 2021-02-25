import pytest
from . simple_api_client import APIClient

import pytest
"""
use 'https://api.openbrewerydb.org/ for command f"pytest -v --url= {} test_dog_ceo.py"
"""

@pytest.mark.parametrize('number', [2, 30, pytest.param(60, marks=pytest.mark.xfail)])
def test_api_check_number_of_messages(api_client, number):
    """
    Check if api returns as many breweries per page as specified in the parameters
    """
    res = api_client.get(path='breweries',params={'per_page':number}).json()
    assert len(res) == number



def test_api_check_fields_list(api_client):
    """
    Check json scheme
    """
    fields = ['id', 'name', 'brewery_type', 'street', 'city', 'state', 'postal_code', 'country', 'longitude',
              'latitude', 'phone', 'website_url', 'updated_at', 'tag_list']
    res = api_client.get(path='breweries', params={'per_page': 1}).json()
    brewery = res[0]
    assert set(brewery.keys()) == set(fields)


@pytest.mark.parametrize('state, expected_state_title', [('new_york', 'New York'), ('colorado', 'Colorado')])
def test_api_check_state_filter(api_client, state, expected_state_title):
    """
    Check if api correctly filter breweries by state
    """
    res = api_client.get(path='breweries', params={'by_state': state}).json()
    states = [brewery['state'] for brewery in res]
    assert set(states) == set([expected_state_title])


@pytest.mark.parametrize('query', ['cat', 'dog'])
def test_api_check_search(api_client, query):
    """
    Check search by name
    """
    res = api_client.get(path='breweries', params={'by_name': query}).json()
    names = [brewery['name'].lower() for brewery in res]
    matched_names = list(filter(lambda name: query in name, names))
    assert len(names) == len(matched_names)


@pytest.mark.parametrize('brewery_id, expected_status_code', [(2, 200), (200000, 404)])
def test_check_api_status_code(api_client, brewery_id, expected_status_code):
    """
    Check if api returns correct status code
    """
    res = api_client.get(path=f'breweries/{brewery_id}')
    assert res.status_code == expected_status_code