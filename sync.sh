#!/bin/bash

s3cmd sync -c s3config .s3ignore --acl-public -M build s3://regenesis.pudo.org
