import asyncio
import aiohttp

# Define a list of dictionaries containing API request details, including proxies when required
api_requests = [
    {
        'url': 'https://api.example.com/endpoint1',
        'method': 'GET',
        'headers': {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'},
        'params': {'param1': 'value1', 'param2': 'value2'},
        'proxy': None  # No proxy for this request
    },
    {
        'url': 'https://api.example.com/endpoint2',
        'method': 'POST',
        'headers': {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'},
        'data': {'key': 'value'},
        'proxy': 'http://proxy-server:port'  # Proxy for this request
    },
    # Add more API requests with different configurations here...
]

async def fetch_data(session, request):
    url = request.get('url')
    method = request.get('method', 'GET')
    headers = request.get('headers', {})
    params = request.get('params', {})
    data = request.get('data')
    proxy = request.get('proxy')

    try:
        async with session.request(method, url, headers=headers, params=params, json=data, proxy=proxy) as response:
            if response.status == 200:
                result = await response.json()
                print(f"Received data from {url}: {result}")
            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status}")
                # Retry logic can be added here if needed
    except aiohttp.ClientError as e:
        print(f"Error fetching data from {url}: {e}")

async def make_requests():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, request) for request in api_requests]
        await asyncio.gather(*tasks)

# Run the event loop to make concurrent requests
asyncio.run(make_requests())
