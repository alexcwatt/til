# Load Balancers

I've been getting a crash course on load balancers lately as we've had some issues with them at work. Our use case is connecting one service to another with gRPC, with Google's Internal Application Load Balancer (ILB) in front of the service we connect to.

Here are a few things I've learned:

* **Layer 4 load balancer and connection stickiness:** When the client opens a persistent connection to the server via the load balancer, the connection will be "sticky" and terminate at a common server backend.
  * For HTTP/1.0, where each request/response involves a fresh connection, this means each new request gets mapped to a new backend.
  * For HTTP/1.1, with keep-alive, the connection can stay open after a request and subsequent requests will route to the same backend.
  * For HTTP/2, if the connection is being used for multiplexed requests, all of the traffic will go to a single backend.
  * In short, you can't _not_ have sticky connections with a Layer 4 load balancer because the TCP connection is the thing that is getting load balanced across backends.
* **Layer 7 differences:** At Layer 7, when the client establishes an HTTP connection, the load balancer can route it based on the HTTP route since it is aware of this layer (e.g., `/api` goes to one pool of backends and `/static` goes to another). In addition, some Layer 7 load balancers can be configured so that different HTTP/2 streams route to different backends, but that is less common than having sticky connections, with all streams on the same connection using a dedicated connection to a particular backend.
* **Backend fullness:** A particular backend's fullness is measured as its current load divided by its capacity. If a load balancer is aware of fullness, it might route traffic towards the least full backend.

At work, we have been observing latency spikes between our gRPC client and server and have traced it to a load balancer that is used for many backends. One of these backends (applications) has traffic spikes and seems to not scale well in response - we can see its backend fullness growing well past 100%. When this happens, some requests to other backends through the load balancer take a hit; requests are queuing up. There are probably a few lessons here, including: (1) latency-sensitive applications should have dedicated load balancers; (2) When sharing a load balancer, a noisy neighbor can affect the others so it is important to monitor backend fullness.
