#!/bin/sh

echo "Waiting for Elasticsearch and Kibana..."

while ! nc -z elasticsearch 9200 && ! nc -z kibana 5601; do
  sleep 0.1
done

echo "Elasticsearch and Kibana started"

# is an array-like construct of all positional parameters. to accept additional parameters
exec "$@"