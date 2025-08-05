# `Symbol#to_s` object allocations

I recently started optimizing a new API at work. I noticed that the p95 time for garbage collection for this API endpoint is 45ms and so I started looking at object allocations. I found ~85,000 object allocations in an example request coming from `Symbol#to_s` from `ParameterFilter` in ActiveSupport!

I asked internally and learned about the [symbol-fstring gem](https://github.com/Shopify/symbol-fstring) that Shopify built which overrides `Symbol#to_s` so that it returns a frozen string and doesn't perform allocations. This should be a great improvement in this particular case because we keep calling `to_s` on the same symbols.
