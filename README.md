This script convert ChhoeTaigiDatabase .csv to OpenVanilla .cin format

pip install -r requirement.txt
git submodule init
git submodule update
python3 processor.py > kip.cin
