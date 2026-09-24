cd src
(
echo ls
echo exit
) | py main.py
(
echo ls
echo cd
echo exit
) | py main.py "default-dir/testVFS.xml" "empty.py"
exit