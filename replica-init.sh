#!/bin/bash
docker exec -it mongo1 mongo --eval "
rs.initiate({
  _id: 'my-replica-set',
  members: [
    { _id: 0, host: 'mongo1:27017' },
    { _id: 1, host: 'mongo2:27017' },
    { _id: 2, host: 'mongo3:27017' }
  ]
})
"