# API Usage Examples

# Payload Example
```
payload = {
    "node0": {"x": x1, "y": y1},
    "node1": {"x": x2, "y": y2}
}
```

## Python Example:
```python

import requests

# Input variables
x1 = 0
y1 = 0
x2 = 5
y2 = 5
limit = 3

# JSON payload
payload = {
    "node0": {"x": x1, "y": y1},
    "node1": {"x": x2, "y": y2}
}

# Headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Make POST request
try:
    response = requests.post(
        'https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit=' + str(limit),
        json=payload,
        headers=headers
    )
    response.raise_for_status()  # Raise an error for unsuccessful responses
    data = response.json()
    print("Next Step:", data['next_step'])
except requests.exceptions.RequestException as e:
    print("Error:", e)
```

## C Example 
```c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <jansson.h>

// Struct to hold response data
struct MemoryStruct {
    char *memory;
    size_t size;
};

// Callback function to write response data
static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    mem->memory = realloc(mem->memory, mem->size + realsize + 1);
    if (mem->memory == NULL) {
        printf("Error: realloc failed\n");
        return 0;
    }

    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

int main() {
    // Input variables
    int x1 = 0;
    int y1 = 0;
    int x2 = 5;
    int y2 = 5;
    int limit = 3;

    CURL *curl;
    CURLcode res;

    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_ALL);

    // Create libcurl handle
    curl = curl_easy_init();
    if (curl) {
        // Construct JSON payload
        json_t *root = json_object();
        json_object_set_new(root, "node0", json_pack("{s:i, s:i}", "x", x1, "y", y1));
        json_object_set_new(root, "node1", json_pack("{s:i, s:i}", "x", x2, "y", y2));
        char *payload = json_dumps(root, JSON_COMPACT);
        json_decref(root);

        // Construct URL with query parameter
        char *url;
        asprintf(&url, "https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit=%d", limit);

        // Set libcurl options
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);

        // Response data
        struct MemoryStruct chunk;
        chunk.memory = malloc(1);
        chunk.size = 0;

        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        // Perform the request
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        } else {
            // Parse JSON response
            json_error_t error;
            json_t *root = json_loads(chunk.memory, 0, &error);
            if (!root) {
                fprintf(stderr, "Error parsing JSON: %s\n", error.text);
            } else {
                json_t *next_step = json_object_get(root, "next_step");
                double x, y;
                json_unpack(next_step, "{s:f, s:f}", "x", &x, "y", &y);
                printf("Next Step: (%f, %f)\n", x, y);
                json_decref(root);
            }
        }

        // Cleanup
        free(chunk.memory);
        free(payload);
        free(url);
        curl_easy_cleanup(curl);
    }

    // Cleanup libcurl
    curl_global_cleanup();

    return 0;
}
```

## C++ Example
```c++

#include <iostream>
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

// Struct to hold response data
struct MemoryStruct {
    char *memory;
    size_t size;
};

// Callback function to write response data
static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    mem->memory = (char *)realloc(mem->memory, mem->size + realsize + 1);
    if (mem->memory == NULL) {
        std::cerr << "Error: realloc failed" << std::endl;
        return 0;
    }

    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

int main() {
    // Input variables
    int x1 = 0;
    int y1 = 0;
    int x2 = 5;
    int y2 = 5;
    int limit = 3;

    CURL *curl;
    CURLcode res;

    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_ALL);

    // Create libcurl handle
    curl = curl_easy_init();
    if (curl) {
        // Construct JSON payload
        std::string payload = "{\"node0\":{\"x\":" + std::to_string(x1) + ",\"y\":" + std::to_string(y1) + "},\"node1\":{\"x\":" + std::to_string(x2) + ",\"y\":" + std::to_string(y2) + "}}";

        // Construct URL with query parameter
        std::string url = "https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit=" + std::to_string(limit);

        // Response data
        struct MemoryStruct chunk;
        chunk.memory = (char *)malloc(1);
        chunk.size = 0;

        // Set libcurl options
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        // Perform the request
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            // Parse JSON response
            json data = json::parse(chunk.memory);
            std::cout << "Next Step: (" << data["next_step"]["x"] << ", " << data["next_step"]["y"] << ")" << std::endl;
        }

        // Cleanup
        free(chunk.memory);
        curl_easy_cleanup(curl);
    }

    // Cleanup libcurl
    curl_global_cleanup();

    return 0;
}
```

## Java Example

```java

import org.json.JSONObject;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) {
        // Input variables
        int x1 = 0;
        int y1 = 0;
        int x2 = 5;
        int y2 = 5;
        int limit = 3;

        // JSON payload
        JSONObject payload = new JSONObject()
                .put("node0", new JSONObject()
                        .put("x", x1)
                        .put("y", y1))
                .put("node1", new JSONObject()
                        .put("x", x2)
                        .put("y", y2));

        // Make POST request
        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit=" + limit))
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(payload.toString()))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                JSONObject data = new JSONObject(response.body());
                JSONObject nextStep = data.getJSONObject("next_step");
                System.out.println("Next Step: (" + nextStep.getDouble("x") + ", " + nextStep.getDouble("y") + ")");
            } else {
                System.out.println("Error: " + response.body());
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

## Javascript Example

```javascript

const fetch = require('node-fetch');

// Input variables
const x1 = 0;
const y1 = 0;
const x2 = 5;
const y2 = 5;
const limit = 3;

// JSON payload
const payload = JSON.stringify({
    node0: { x: x1, y: y1 },
    node1: { x: x2, y: y2 }
});

// Request parameters
const requestOptions = {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: payload
};

// Make POST request
fetch(`https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit=${limit}`, requestOptions)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Next Step:", data.next_step);
    })
    .catch(error => {
        console.error("Error:", error);
    });
```

## Rust Example

```rust

use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Input variables
    let x1 = 0;
    let y1 = 0;
    let x2 = 5;
    let y2 = 5;
    let limit = 3;

    // JSON payload
    let payload = json!({
        "node0": {"x": x1, "y": y1},
        "node1": {"x": x2, "y": y2}
    });

    // Make POST request
    let client = reqwest::Client::new();
    let response = client
        .post("https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d")
        .query(&[("limit", &limit.to_string())])
        .json(&payload)
        .send()
        .await?;

    // Check if response is successful
    if response.status().is_success() {
        // Parse response JSON
        let data: serde_json::Value = response.json().await?;
        // Print next_step
        if let Some(next_step) = data.get("next_step") {
            println!("Next Step: {}", next_step);
        } else {
            println!("Next Step not found in response.");
        }
    } else {
        println!("Error: {}", response.status());
    }

    Ok(())
}
```

## Go Example

```go

package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	// Input variables
	x1 := 0
	y1 := 0
	x2 := 5
	y2 := 5
	limit := 3

	// JSON payload
	payload := map[string]interface{}{
		"node0": map[string]int{"x": x1, "y": y1},
		"node1": map[string]int{"x": x2, "y": y2},
	}

	// Convert payload to JSON
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}

	// Make POST request
	url := fmt.Sprintf("https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit=%d", limit)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(payloadBytes))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	// Set headers
	req.Header.Set("Accept", "application/json")
	req.Header.Set("Content-Type", "application/json")

	// Create HTTP client and send request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making request:", err)
		return
	}
	defer resp.Body.Close()

	// Check if response is successful
	if resp.StatusCode != http.StatusOK {
		fmt.Println("Error:", resp.Status)
		return
	}

	// Decode response JSON
	var data map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Println("Error decoding JSON:", err)
		return
	}

	// Print next_step
	nextStep, ok := data["next_step"].(string)
	if !ok {
		fmt.Println("Next Step not found in response.")
		return
	}
	fmt.Println("Next Step:", nextStep)
}
```

## Swift Example

```swift

import Foundation

// Input variables
let x1 = 0
let y1 = 0
let x2 = 5
let y2 = 5
let limit = 3

// JSON payload
let payload = [
    "node0": ["x": x1, "y": y1],
    "node1": ["x": x2, "y": y2]
]

// Convert payload to Data
guard let payloadData = try? JSONSerialization.data(withJSONObject: payload) else {
    print("Error converting payload to Data.")
    exit(1)
}

// Request URL
let urlString = "https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit=\(limit)"
guard let url = URL(string: urlString) else {
    print("Error creating URL.")
    exit(1)
}

// Create URLRequest
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("application/json", forHTTPHeaderField: "Content-Type")
request.setValue("application/json", forHTTPHeaderField: "Accept")
request.httpBody = payloadData

// Perform the request
let task = URLSession.shared.dataTask(with: request) { data, response, error in
    // Check for errors
    if let error = error {
        print("Error:", error)
        return
    }
    
    // Check for response
    guard let httpResponse = response as? HTTPURLResponse else {
        print("Error: No HTTP response")
        return
    }
    
    // Check for successful response
    guard (200...299).contains(httpResponse.statusCode) else {
        print("Error: HTTP status code \(httpResponse.statusCode)")
        return
    }
    
    // Check if there is data
    guard let responseData = data else {
        print("Error: No response data")
        return
    }
    
    // Parse JSON response
    do {
        if let jsonResponse = try JSONSerialization.jsonObject(with: responseData, options: []) as? [String: Any],
           let nextStep = jsonResponse["next_step"] as? String {
            print("Next Step:", nextStep)
        } else {
            print("Error: Couldn't find next_step in JSON response")
        }
    } catch {
        print("Error parsing JSON response:", error)
    }
}

task.resume()
```

## C# Example

```c#

using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // Input variables
        int x1 = 0;
        int y1 = 0;
        int x2 = 5;
        int y2 = 5;
        int limit = 3;

        // JSON payload
        var payload = new
        {
            node0 = new { x = x1, y = y1 },
            node1 = new { x = x2, y = y2 }
        };

        // Convert payload to JSON
        var payloadJson = JsonSerializer.Serialize(payload);
        var content = new StringContent(payloadJson, System.Text.Encoding.UTF8, "application/json");

        // Make POST request
        using var client = new HttpClient();
        var url = $"https://bellanderoboticssensorsresearchinnovationcenter-kot42qxp.b4a.run/api/Bellande_Step/bellande_step_2d?limit={limit}";
        try
        {
            var response = await client.PostAsync(url, content);
            response.EnsureSuccessStatusCode(); // Throws exception for unsuccessful responses

            // Parse JSON response
            var responseContent = await response.Content.ReadAsStringAsync();
            var responseData = JsonSerializer.Deserialize<dynamic>(responseContent);

            // Print next_step
            Console.WriteLine("Next Step: " + responseData.next_step);
        }
        catch (HttpRequestException e)
        {
            Console.WriteLine("Error: " + e.Message);
        }
    }
}
```
