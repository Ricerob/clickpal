conda create -n spleeter-env python=3.9 --no-default-packages
conda activate spleeter-env
conda install -c conda-forge ffmpeg tensorflow=2.9 numba
pip install -r requirements.txt

add songs in examples then run the junt. YUHHH

TODO:
- PyAudacity implementation
- dockerize? executable perhaps? GUI?