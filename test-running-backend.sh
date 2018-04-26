#!/bin/bash

export SINAMECC_USERNAME=admin
export SINAMECC_PASSWORD=cambiame
curl -XGET -H "Content-Type: application/json" -H"Authorization: $(./get_token)" http://localhost:8000/api/v1/user/admin
