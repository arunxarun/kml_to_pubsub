to get up and running:
requirements:
* a service-key.json in the key directory
* a valid GOOGLE_PROJECT_ID in app.yml
* a valid PUBSUB_TOPIC in app.yml

instructions:
* docker build .
* docker run -d -t kml-pubsub -p 5000:5000
* cd src
* curl -H "Content-Type: application/json" -X POST --data-binary  @./test_data/short_kml_file.json "http://localhost:5000/publish?batch_size=10&offset=2&uuid=1234"

OR

* docker run -d  arunxarun/kml-pubsub:latest
* curl -H "Content-Type: application/json" -X POST --data-binary  @./test_data/short_kml_file.json "http://localhost:5000/publish?batch_size=10&offset=2&uuid=1234"
