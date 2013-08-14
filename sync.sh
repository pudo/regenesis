#!/bin/bash

s3cmd sync -c s3config .s3ignore --acl-public --guess-mime-type --no-progress build/* s3://regenesis.pudo.org
