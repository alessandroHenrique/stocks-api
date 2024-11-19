LAYER_NAME := beautifulsoup4-layer
REGION := us-east-1
PROFILE := default

build:
	bash build.sh

upload:
	aws lambda publish-layer-version \
		--layer-name $(LAYER_NAME) \
		--description "Python 3.10 layer for beautifulsoup4 library" \
		--compatible-runtimes python3.10 \
		--region $(REGION) \
		--zip-file fileb://$(LAYER_NAME).zip \
		--profile $(PROFILE)

clean:
	rm -rf python $(LAYER_NAME).zip
