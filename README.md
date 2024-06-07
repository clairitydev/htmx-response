# FastAPI HTMX Integration

This Python package provides a custom route handler for FastAPI applications that supports content negotiation and dynamic rendering with HTMX and Jinja2 templates. This allows responses to be conditionally rendered as HTML or JSON based on the `Accept` header in the request.

## Features

- **Content Negotiation**: Automatically serves HTML or JSON responses based on the client's `Accept` header.
- **HTMX Support**: Integrates HTMX for partial page updates with server-side rendering.
- **Dynamic Jinja2 Rendering**: Uses Jinja2 templates to render HTML responses based on JSON data.

## Requirements

- Python 3.6+
- FastAPI
- Jinja2
- accept_types

## Installation

Install the package using pip:

```bash
pip install fastapi-htmx-integration
```

# Usage

To use the HTMX route handler in your FastAPI application:

Define the base directory for your Jinja2 templates.
Specify the base template file.
Use the get_htmx_route function to create routes in your FastAPI app.

```
from fastapi import FastAPI
from your_package_name import get_htmx_route

app = FastAPI()

# Define the HTMX route
app.router.route_class = get_htmx_route(base_dir='templates', base_template='layout.html')

@app.get("/")
async def root():
    return {"message": "Hello World"}

# More routes can be defined here
```