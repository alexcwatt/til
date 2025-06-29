# mDNS

Multicast DNS (mDNS) allows devices on a local network to discover each other. It's how you can find printers on the local network, as one example.

I recently was configuring [snapcast](https://github.com/badaix/snapcast) and trying to run the mazzolino/librespot-snapserver Docker image so I can stream music from Spotify to speakers in my home, without depending on a vendor like Sonos. I was having trouble getting Spotify to discover my Snapcast speaker as a Spotify Connect output option.

I learned (from sending some log messages to ChatGPT) that what I was missing was `network_mode: host` in my docker-compose.yml file. This option makes the container share the host's network stack directly, including its mDNS setup for service discovery. Once I changed that option, Spotify was able to see my new Spotify Connect output.
