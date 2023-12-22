setup:
	python3 -m venv .env && source env/bin/activate

install-requirements:
	pip3 install -r requirements.txt

build:
	pyinstaller --onefile --paths=/env/Lib/site-packages src/main.py
	mv dist/main dist/petitepass
	cp dist/petitepass petitepass_package/bin/petitepass

install:
	mkdir /opt/PetitePass && cp dist/PetitePass /usr/bin/PetitePass

uninstall:
	rm -rf /opt/PetitePass && rm -rf /usr/bin/PetitePass

clean:
	rm -rf build dist
