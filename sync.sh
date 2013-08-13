#!/bin/bash

s3cmd sync -c s3config .s3ignore --acl-public --guess-mime-type build/* s3://regenesis.pudo.org
