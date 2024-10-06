#!/bin/bash

# Function to take a screenshot
take_screenshot() {
    echo "🕣 Waiting for taking a screenshot"
    echo
    if [[ "$OSTYPE" == "darwin"* ]]; then
        screencapture -i screenshot.png
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows - using PowerShell to take a screenshot
        powershell.exe -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%{PRTSC}'); Start-Sleep -Milliseconds 500; [System.Windows.Forms.Clipboard]::GetImage().Save('screenshot.png');"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux - using scrot or gnome-screenshot
        if command -v scrot &>/dev/null; then
            scrot -s 'screenshot.png'
        elif command -v gnome-screenshot &>/dev/null; then
            gnome-screenshot -a -f 'screenshot.png'
        elif command -v import &>/dev/null; then
            import root 'screenshot.png'
        else
            echo "No screenshot tool found. Please install scrot, gnome-screenshot, or ImageMagick."
            exit 1
        fi
    else
        echo "Unsupported OS."
        exit 1
    fi
    echo "✅ Screenshot taken"
    echo
}

# Check if curl is installed
if ! command -v curl &>/dev/null; then
    echo "curl is not installed. Please install it using your package manager."
    exit 1
fi

# Check if jq is installed
if ! command -v jq &>/dev/null; then
    echo "jq is not installed. Please install it using your package manager."
    exit 1
fi

take_screenshot

echo "🏭 Processing image"
echo
IMG_URL=$(curl -F "image=@screenshot.png" -F "key=f19625ab3b053070e82d9943aff9e1e9" -F "expiration=600" https://api.imgbb.com/1/upload -s | jq -r '.data.url')
ENCODED_URL=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$IMG_URL'''))")
echo "✅ Image processed"
echo

echo "🚀 Opening results in google lens"
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "https://lens.google.com/uploadbyurl?url=$ENCODED_URL"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start "https://lens.google.com/uploadbyurl?url=$ENCODED_URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "https://lens.google.com/uploadbyurl?url=$ENCODED_URL"
else
    echo "Unsupported OS."
    exit 1
fi
