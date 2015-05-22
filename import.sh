
if [ "$1" == "P" ]; then
    data="{\"Path\": \"$2\"}"
else
    data="{\"Src\": \"$2\", \"Dst\": \"$3\"}"
fi

echo $data

curl -H "Content-Type: application/json" -X POST -d "$data" http://localhost:8000/import

echo ""