# Load Balancers

I've been getting a crash course on load balancers lately as we've had some issues with them at work. Our use case is connecting one service to another with gRPC, with Google's Internal Application Load Balancer (ILB) in front of the service we connect to.

## Layer 4 vs. Layer 7 Load Balancers

Layer 4 load balancers operate at the transport level. An incoming TCP connection will terminate at a specific server backend and remain "sticky" for the duration of the connection:

* For HTTP/1.0, where each request/response involves a fresh connection, each request gives the load balancer the opportunity to choose a backend.
* For HTTP/1.1, with keep-alive, the connection can stay open after a request and subsequent requests will route to the same backend.
* For HTTP/2, if the connection is being used for multiplexed requests, all of the traffic will go to a single backend.

Layer 7 load balancers operate at the application layer. This allows the load balancer to be more sophisticated:

* The load balancer can route based on the URL (e.g., `/api` goes to one pool of backends and `/static` goes to another), since it understands HTTP.
* With HTTP/1.1 and HTTP/2, you can have a long-standing connection but the load balancer can spread requests across multiple backends.

## Backend Fullness

I learned that "backend fullness" measures the current load on a backend divided by its capacity. If a load balancer is aware of fullness, it might route traffic towards the least full backend.

At work, we observed latency spikes between a gRPC client and server and traced it to a load balancer that is used for many backends. One of these backends (applications) had traffic spikes and did not scale out in response - we could see its backend fullness growing well past 100%. When this happens, some requests to other backends through the load balancer took a hit; requests were queuing up. There are probably a few lessons here, including: (1) latency-sensitive applications should have dedicated load balancers; (2) when sharing a load balancer, a noisy neighbor can affect the others so it is important to monitor backend fullness.

## Horizontal Scaling and Load Balancers

Regardless of whether a layer 4 or layer 7 load balancer is used, it is expected that a connection will be routed through a single proxy server.

Imagine a scale-out situation: Your service is seeing increased load and crosses a threshold. In response, the number of backends in the pool scales out, and so do the number of proxies for the load balancer.

If you have persistent connections to the backend through the load balancer, these connections will remain "sticky" to particular proxies, and the scale-out could cause issues. At work, we saw an issue where a scaling event happened - but because we had persistent connections from a fixed pool of clients via our load balancers, the load was stuck on particular Envoy proxies, and we saw increased latency for the traffic going through those proxies.

While persistent connections are useful because they reduce the overhead in making requests, it seems like a good idea to recycle connections occasionally to spread load across the proxies that do the load balancing.

### `GOAWAY`

Note that an HTTP/2 proxy like Envoy might use `GOAWAY` frames to initiate a graceful shutdown. So in the case described, where a single proxy becomes a hotspot, the proxy could send `GOAWAY` informing the client to gracefully end the connection and establish a new connection through the load balancer.
