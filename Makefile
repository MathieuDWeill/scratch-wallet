.PHONY: run check rpc deploy package

run:
	streamlit run app.py

check:
	python -m compileall app.py engine scripts

rpc:
	python scripts/check_hashkey_rpc.py

deploy:
	npm run compile && npm run test && npm run deploy:hashkey

package:
	cd .. && zip -r scratch-wallet-streamlit-mathieu-d-weill.zip scratch-wallet-streamlit -x 'scratch-wallet-streamlit/.env' 'scratch-wallet-streamlit/node_modules/*' 'scratch-wallet-streamlit/__pycache__/*' 'scratch-wallet-streamlit/engine/__pycache__/*' 'scratch-wallet-streamlit/.streamlit/secrets.toml'


record-video:
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-video.txt
	python -m playwright install chromium
	python scripts/record_demo_playwright.py --start-app

video-from-screenshots:
	python scripts/make_video_from_screenshots.py --screenshots demo_recordings/latest/screenshots --out demo_recordings/fallback.mp4

finalize:
	python scripts/one_click_final.py --skip-video

finalize-video:
	python scripts/one_click_final.py
