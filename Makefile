install-requirements:
	virtualenv env && source env/bin/activate && pip3 install -r requirements.txt

build:
	pyinstaller --onefile --paths=/env/Lib/site-packages password-manager.py

install:
	mkdir /opt/password-manager && cp dist/password-manager /usr/bin/password-manager

uninstall:
	rm -rf /opt/password-manager && rm -rf /usr/bin/password-manager

clean:
	rm -rf build dist