SHELL := /bin/bash

LAMBDA_NAME = polygon_data
BUCKET_NAME = stocks-api
REGION = us-east-1
PROFILE := default

clean:
	@rm -rf $(LAMBDA_NAME).zip
	@echo "Done!!"

zip:
	@zip $(LAMBDA_NAME).zip lambda_function.py
	@echo "Done!!"

upload:
	@aws s3 cp $(LAMBDA_NAME).zip s3://$(BUCKET_NAME)/lambda/functions/$(LAMBDA_NAME).zip
	@echo "Done!!"

update: zip upload clean
	@aws lambda update-function-code --function-name $(LAMBDA_NAME) --s3-bucket $(BUCKET_NAME) --s3-key lambda/functions/$(LAMBDA_NAME).zip
	@echo "Done!!"
