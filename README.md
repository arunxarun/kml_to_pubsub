to get up and running:
requirements:
1. a service-key.json in the key directory
2. a valid GOOGLE_PROJECT_ID in app.yml
3. a valid PUBSUB_TOPIC in app.yml

instructions:
1. docker build .
2. docker run -d -t kml-pubsub -p 5000:5000
3. cd src
4. curl -H "Content-Type: application/json" -X POST --data-binary  @./test_data/short_kml_file.json "http://localhost:5000/publish?batch_size=10&offset=2&uuid=1234"

OR

1. docker run -d  arunxarun/kml-pubsub:latest
2. curl -H "Content-Type: application/json" -X POST --data-binary  @./test_data/short_kml_file.json "http://localhost:5000/publish?batch_size=10&offset=2&uuid=1234"
