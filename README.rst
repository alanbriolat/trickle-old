========================================
Trickle - A minimalist web UI for Deluge
========================================

Trickle is a minimalist web UI for Deluge for use in situations where the heavyweight format of the 
official Deluge web UI is inappropriate, for example on mobile phones.  It aims to provide all of 
the essential functionality without aiming to have an "application-like" feel.  Certain aspects of 
dynamic update may be added at a later date.

Trickle depends on jsonrpclib.  The necessary fork of jsonrpclib is available at 
http://github.com/alanbriolat/jsonrpclib/, improving JSON-RPC 1.0 conformance and supporting cookies 
(necessary for Deluge's API authentication).
