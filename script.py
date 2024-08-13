import asyncio
import aiohttp
import time


async def post_data(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.text()


async def make_requests(url, num_requests, data):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            task = asyncio.ensure_future(post_data(session, url, data))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        return responses


def main():
    url = "http://127.0.0.1:8000/reservation/get-ticket"
    num_requests = 100
    data = {
        'patient_id': 1,
        'doctor_id': 1,
    }

    start_time = time.time()
    responses = asyncio.run(make_requests(url, num_requests, data))
    end_time = time.time()

    for i, response in enumerate(responses):
        print(f"Response {i+1}: {response[:100]}...")
    
    print(f"Sent {num_requests} POST requests in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
