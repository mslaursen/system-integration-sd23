# Webhook Customer Support Service Integration Guide

This is an integration guide, that outlines how to integrate your system with this service to receive events about ticket events and service status changes.

## Getting Started

To integrate with this service, you'll need an endpoint that can handle HTTP POST requests. This endpoint should be able to process JSON payloads.

## Webhooks

### Registering Your Webhook

To start receiving events, register your callback URL with the service.

- **Endpoint:** `/webhooks/register`
- **Method:** `POST`

- **Request Body:**

```json
{
  "callback_url": "https://yourdomain.com/webhook/endpoint"
}
```

- **Successful response:**
```json
{
  "data": {
    "id": "webhook_id"
  }
}
```

### Unregistering Your Webhook

To stop receiving events, you can unregister your webhook.

- **Endpoint:** `/webhooks/unregister/{webhook_id}`
- **Method:** `DELETE`

### Viewing Registered Webhooks

To see all registered webhooks:

- **Endpoint:** `/webhooks`
- **Method:** `GET`

### Testing Webhooks

Send a ping event to all registered webhooks:

- **Endpoint:** `/webhooks/ping`
- **Method:** `POST`
- *Emits a `ping` event.*

## Managing Tickets

### Creating a Ticket

To open a new ticket:

- **Endpoint:** `/tickets`
- **Method:** `POST`
- *Emits a `ticket_opened` event.*
- **Request Body:**

```json
{
  "ticket_message": "Your issue description."
}
```

- **Successful Response:**

```json
{
  "data": {
    "id": "ticket_id"
  }
}
```

### Closing a Ticket

To close an existing ticket:

- **Endpoint:** `/tickets/{ticket_id}`
- **Method:** `DELETE`
- *Emits a `ticket_closed` event.*

### Updating a Ticket

To update the message of an existing ticket:

- **Endpoint:** `/tickets/{ticket_id}`
- **Method:** `PATCH`
- *Emits a `ticket_updated` event.*
- **Request Body:**

```json
{
  "ticket_message": "Updated issue description."
}
```

### Retrieving All Tickets

To list all tickets:

- **Endpoint:** `/tickets`
- **Method:** `GET`

## Service Status

### Marking Service as Unavailable

To indicate the service is currently down:

- **Endpoint:** `/service/unavailable`
- **Method:** `POST`
- *Emits a `service_unavailable` event.*

### Marking Service as Available

To indicate the service is back online:

- **Endpoint:** `/service/available`
- **Method:** `POST`
- *Emits a `service_available` event.*

## Event Notifications

Your registered webhook endpoint will receive JSON payloads for various events.

### Example Payload

```json
{
  "event": "ticket_opened",
  "created": "2023-01-01T00:00:00Z",
  "data": {
    "ticket_message": "Issue description."
  }
}
```

### Supported Event Types

- `ticket_opened`: Notifies when a new ticket is created.
- `ticket_closed`: Notifies when a ticket is closed.
- `ticket_updated`: Notifies when a ticket is updated.
- `service_unavailable`: Indicates the service is unavailable.
- `service_available`: Indicates the service is available again.
- `ping`: Used for testing webhook connections.






## Event Response Format

This service notifies your system about various events via webhooks. Depending on the event type, the notification may include specific data relevant to the event.

### Event Response Format

All event notifications share a common JSON structure:

```json
{
  "event": "EventType",
  "created": "Timestamp",
  "data": {}
}
```

- `event`: A string indicating the type of event. See [Supported Event Types](#supported-event-types) for more details.
- `created`: The UTC timestamp when the event was generated.
- `data`: An object containing event-specific data. This field may be empty (`{}`) for events that do not include additional data.

### Events With Data

Some events include specific data relevant to the occurrence:

- **ticket_opened**: Sent when a new ticket is created.
  - `data`: Contains the `ticket_message`.
- **ticket_updated**: Sent when a ticket's message is updated.
  - `data`: Contains the updated `ticket_message`.

### Example: Ticket Opened Event

Here's an example payload for a `ticket_opened` event:

```json
{
  "event": "ticket_opened",
  "created": "2023-01-01T12:00:00Z",
  "data": {
    "ticket_message": "User cannot access the dashboard."
  }
}
```
