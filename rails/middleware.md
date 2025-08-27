# Middleware

Middleware order matters! As an example, I was adjusting the integration of [app_profiler](https://github.com/Shopify/app_profiler) in a Rails app and turned on a setting for otel instrumentation, but it wasn't working. When I dug in, I realized the OpenTelemetry middleware was running after the AppProfiler middleware, so profiling happened before instrumentation and we couldn't attach the profile metadata to the span.

Some learnings:

* You can use `bin/rails middleware` to get the ordered list of middleware.
* It might make sense to write a test for the exact middleware in your app and the order, to prevent unintended changes.
* You can use `app.config.middleware.move_before` and `move_after` to shift middleware ordering, and you can use an initializer that runs after another specific initializer so that you don't try to reorder the middleware before it has all been injected.
