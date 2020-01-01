#!/bin/bash
heroku container:push web -a perdana-indonesia
heroku container:release web -a perdana-indonesia
