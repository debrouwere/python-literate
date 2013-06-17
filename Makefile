all:
	rm -rf ./build
	mkdir -p ./build/resources/{scripts,styles}
	coffee -cbo ./build/resources/scripts ./literate/templates/scripts
	stylus -o ./build/resources/styles ./literate/templates/styles