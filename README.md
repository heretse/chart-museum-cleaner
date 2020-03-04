# chart-museum-cleaner
Keep only recent chart versions in chart museum. You give number of recent chart versions to keep in a parameter


## Getting started
#### Use as a container
Run the following, and you will see the command description

`docker run --rm --network=host chart-museum-cleaner`

##### Delete unsuded chart versions
The following command keep 4 versions for each chart.

`docker run --rm --network=host chart-museum-cleaner delete --keep 4`

It requires a local chart museum, for example, by `docker-compose up`

#### Set a different chart museum and token

`docker run --rm -e CHART_MUSEUM_URL=https://helm-charts -e TOKEN='' chart-museum-cleaner delete --keep 10`

- Without a token, you will see the following message:

`Fail to delete chart: shipment-service, version: 1.1.41183, status: 401, reason: Unauthorized`
