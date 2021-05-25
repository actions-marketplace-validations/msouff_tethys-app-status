#!/bin/sh -l

echo -e "\033[1;4;34mInstallation Status.\033[0m"
PYTHON_OUTPUT=$(python "/tethys_app_status.py" "$1" "$2" "$3")

echo "$PYTHON_OUTPUT"

RESULT=$(echo "$PYTHON_OUTPUT" | awk -F'RESULT: ' '{print $2}')

case $RESULT in
  *"Failed"*)
    exit 1
    ;;
esac
