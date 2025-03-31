# #!/usr/bin/env python3
# import requests
# import json
# import time
# import concurrent.futures
# #
# # -------------------------------
# # Configuration
# # -------------------------------
# URL = "http://127.0.0.1:5000/predict"
# PAYLOAD = {
#     "gender": "Male",
#     "race": "White",
#     "age_at_release": 35,
#     "education_level": "High School",
#     "supervision_risk_score_first": 0.3,
#     "residence_puma": "12345",
#     "jobs_per_year": 2
# }
# HEADERS = {"Content-Type": "application/json"}

# # -------------------------------
# # Utility function to send one POST request
# # -------------------------------
# def send_request():
#     """Send a single POST request to the API endpoint."""
#     try:
#         response = requests.post(URL, data=json.dumps(PAYLOAD), headers=HEADERS)
#         return response.json()
#     except Exception as e:
#         return {"error": str(e)}

# # -------------------------------
# # Performance Testing Function
# # -------------------------------
# def performance_test(num_requests=100, concurrency=10):
#     """
#     Send a fixed number of requests using a specified level of concurrency
#     and measure the total time taken.
#     """
#     print(f"\n[Performance Test] {num_requests} requests with concurrency={concurrency}")
#     start_time = time.time()

#     with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
#         # Submit all requests concurrently.
#         futures = [executor.submit(send_request) for _ in range(num_requests)]
#         # Wait for all futures to complete.
#         results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
#     total_time = time.time() - start_time
#     print(f"Total time: {total_time:.2f} seconds for {num_requests} requests")
#     return total_time, results

# # -------------------------------
# # Scalability Testing Function
# # -------------------------------
# def scalability_test():
#     """
#     Gradually increase the concurrency level and log the total and average response time.
#     """
#     print("\n[Scalability Test] Starting scalability testing...")
#     # Define a set of concurrency levels to test.
#     concurrency_levels = [5, 10, 20, 50, 100]
#     # We'll use a modest number of requests per test for demonstration.
#     num_requests = 50  
#     results_summary = {}

#     for concurrency in concurrency_levels:
#         print(f"\n-- Testing with concurrency level: {concurrency} --")
#         total_time, _ = performance_test(num_requests, concurrency)
#         avg_time = total_time / num_requests
#         results_summary[concurrency] = (total_time, avg_time)
#         print(f"Concurrency {concurrency}: Total time = {total_time:.2f} sec, "
#               f"Average time per request = {avg_time:.4f} sec")

#     print("\nScalability Test Summary:")
#     for concurrency, (total, avg) in results_summary.items():
#         print(f"  Concurrency {concurrency}: Total Time = {total:.2f} sec, Avg Time = {avg:.4f} sec")

# # -------------------------------
# # Reliability Testing Function
# # -------------------------------
# def reliability_test(duration_seconds=60, delay=1):
#     """
#     Continuously send requests for a given duration to test the API's reliability.
    
#     :param duration_seconds: Total duration to run the test.
#     :param delay: Delay (in seconds) between consecutive requests.
#     """
#     print(f"\n[Reliability Test] Running for {duration_seconds} seconds with {delay}s delay between requests.")
#     start_time = time.time()
#     end_time = start_time + duration_seconds
#     request_count = 0
#     error_count = 0
#     response_times = []

#     while time.time() < end_time:
#         request_count += 1
#         req_start = time.time()
#         try:
#             response = requests.post(URL, data=json.dumps(PAYLOAD), headers=HEADERS)
#             # Optionally, you can process response.json() here.
#             _ = response.json()
#         except Exception as e:
#             error_count += 1
#             print(f"Request #{request_count} failed: {e}")
#         req_end = time.time()
#         response_times.append(req_end - req_start)
#         time.sleep(delay)

#     total_duration = time.time() - start_time
#     avg_response_time = sum(response_times) / len(response_times) if response_times else float('inf')

#     print("\nReliability Test Completed:")
#     print(f"  Total requests sent: {request_count}")
#     print(f"  Total errors: {error_count}")
#     print(f"  Average response time: {avg_response_time:.4f} sec")
#     print(f"  Total test duration: {total_duration:.2f} sec")

# # -------------------------------
# # Main function to run all tests
# # -------------------------------
# def main():
#     # Performance Test
#     performance_test(num_requests=100, concurrency=10)

#     # Scalability Test
#     scalability_test()

#     # Reliability Test
#     # For demonstration, we'll run this test for 60 seconds.
#     reliability_test(duration_seconds=60, delay=1)

# if __name__ == '__main__':
#     main()

#!/usr/bin/env python3
import requests
import json
import time
import concurrent.futures

# -------------------------------
# Configuration
# -------------------------------
URL = "http://127.0.0.1:5000/predict"
PAYLOAD = {
    "gender": "Male",
    "race": "White",
    "age_at_release": 35,
    "education_level": "High School",
    "supervision_risk_score_first": 0.3,
    "residence_puma": "12345",
    "jobs_per_year": 2
}
HEADERS = {"Content-Type": "application/json"}

# -------------------------------
# Utility function to send one POST request
# -------------------------------
def send_request():
    """Send a single POST request to the API endpoint."""
    try:
        response = requests.post(URL, data=json.dumps(PAYLOAD), headers=HEADERS)
        # If the response is not 200 OK, return an error
        if response.status_code != 200:
            return {"error": f"Status code {response.status_code}: {response.text}"}
        try:
            return response.json()
        except ValueError:
            return {"error": f"Non-JSON response: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Performance Testing Function
# -------------------------------
def performance_test(num_requests=100, concurrency=10):
    """
    Send a fixed number of requests using a specified concurrency level
    and measure the total time taken.
    """
    print(f"\n[Performance Test] {num_requests} requests with concurrency={concurrency}")
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit all requests concurrently.
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        # Wait for all futures to complete.
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f} seconds for {num_requests} requests")
    return total_time, results

# -------------------------------
# Scalability Testing Function
# -------------------------------
def scalability_test():
    """
    Gradually increase the concurrency level and log the total and average response time.
    """
    print("\n[Scalability Test] Starting scalability testing...")
    # Define a set of concurrency levels to test.
    concurrency_levels = [5, 10, 20, 50, 100]
    # We'll use a modest number of requests per test for demonstration.
    num_requests = 50  
    results_summary = {}

    for concurrency in concurrency_levels:
        print(f"\n-- Testing with concurrency level: {concurrency} --")
        total_time, _ = performance_test(num_requests, concurrency)
        avg_time = total_time / num_requests
        results_summary[concurrency] = (total_time, avg_time)
        print(f"Concurrency {concurrency}: Total time = {total_time:.2f} sec, "
              f"Average time per request = {avg_time:.4f} sec")

    print("\nScalability Test Summary:")
    for concurrency, (total, avg) in results_summary.items():
        print(f"  Concurrency {concurrency}: Total Time = {total:.2f} sec, Avg Time = {avg:.4f} sec")

# -------------------------------
# Reliability Testing Function
# -------------------------------
def reliability_test(duration_seconds=60, delay=1):
    """
    Continuously send requests for a given duration to test the API's reliability.
    This version checks HTTP status codes and handles non-JSON responses.
    
    :param duration_seconds: Total duration to run the test.
    :param delay: Delay (in seconds) between consecutive requests.
    """
    print(f"\n[Reliability Test] Running for {duration_seconds} seconds with {delay}s delay between requests.")
    start_time = time.time()
    end_time = start_time + duration_seconds
    request_count = 0
    error_count = 0
    response_times = []

    while time.time() < end_time:
        request_count += 1
        req_start = time.time()
        try:
            response = requests.post(URL, data=json.dumps(PAYLOAD), headers=HEADERS)
            if response.status_code != 200:
                print(f"Request #{request_count} error: Status code {response.status_code}, Response: {response.text}")
                error_count += 1
            else:
                try:
                    _ = response.json()
                except ValueError:
                    print(f"Request #{request_count} error: Non-JSON response: {response.text}")
                    error_count += 1
        except Exception as e:
            print(f"Request #{request_count} exception: {e}")
            error_count += 1
        req_end = time.time()
        response_times.append(req_end - req_start)
        time.sleep(delay)

    total_duration = time.time() - start_time
    avg_response_time = sum(response_times) / len(response_times) if response_times else float('inf')

    print("\nReliability Test Completed:")
    print(f"  Total requests sent: {request_count}")
    print(f"  Total errors: {error_count}")
    print(f"  Average response time: {avg_response_time:.4f} sec")
    print(f"  Total test duration: {total_duration:.2f} sec")

# -------------------------------
# Main function to run all tests
# -------------------------------
def main():
    # Performance Test
    performance_test(num_requests=100, concurrency=10)

    # Scalability Test
    scalability_test()

    # Reliability Test (adjust duration and delay as needed)
    reliability_test(duration_seconds=60, delay=1)

if __name__ == '__main__':
    main()
