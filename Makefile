setup:
	virtualenv env && source env/bin/activate

install-requirements:
	pip3 install -r requirements.txt

build:
	pyinstaller --onefile --paths=/env/Lib/site-packages src/main.py

install:
	mkdir /opt/PetitePass && cp dist/PetitePass /usr/bin/PetitePass

uninstall:
	rm -rf /opt/PetitePass && rm -rf /usr/bin/PetitePass

clean:
	rm -rf build dist
