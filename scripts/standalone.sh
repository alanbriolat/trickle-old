#!/bin/bash
export PYTHONPATH="`dirname $0`/../jsonrpclib/"
exec python -m trickle.webui $*
