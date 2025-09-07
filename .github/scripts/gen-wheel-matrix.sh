#!/usr/bin/env bash
#set -euo pipefail

MODE="$1"

# get the right versions and other flags for cibuildwheel

if [[ "$MODE" == "legacy" ]]; then
    CIBW_VERSION="2.23.3"
    GREP_FLAGS=""
    GREP_PATTERN="cp36|cp37"
elif [[ "$MODE" == "modern" ]]; then
    # Extract version from .github/requirements-ci.txt
    CIBW_VERSION=$(grep '^cibuildwheel==' .github/requirements-ci.txt | cut -d= -f3)
    echo $CIBW_VERSION
    if [[ -z "$CIBW_VERSION" ]]; then
        echo "Failed to extract cibuildwheel version from requirements-ci.txt"
        exit 1
    fi
    GREP_FLAGS="-v"
    GREP_PATTERN="cp36|cp37"
    export CIBW_ENABLE="pypy-eol"
else
    echo "Unsupported mode: $MODE (expected 'legacy' or 'modern')"
    exit 2
fi

# do the uninstall/reinstallation of the right version of cibuildwheel
pipx uninstall cibuildwheel
pipx install cibuildwheel==${CIBW_VERSION}

# Handle fast CI case
if [[ "${CI_ONLY:-false}" == "true" ]]; then
    if [[ "$MODE" == "modern" ]]; then
        FIXED_CI_MATRIX=$(jq -n -c --arg ver "$CIBW_VERSION" '
          [
            {"only":"cp313-manylinux_x86_64","os":"ubuntu-22.04","cibw_version": $ver},
            {"only":"cp313-manylinux_aarch64","os":"ubuntu-22.04-arm","cibw_version": $ver},
            {"only":"cp313-musllinux_x86_64","os":"ubuntu-22.04","cibw_version": $ver},
            {"only":"cp313-musllinux_aarch64","os":"ubuntu-22.04-arm","cibw_version": $ver},
            {"only":"cp313-win_amd64","os":"windows-2022","cibw_version": $ver},
            {"only":"cp313-win_arm64","os":"windows-2022","cibw_version": $ver},
            {"only":"cp313-macosx_x86_64","os":"macos-13","cibw_version": $ver},
            {"only":"cp313-macosx_arm64","os":"macos-14","cibw_version": $ver},
            {"only":"cp314-manylinux_x86_64","os":"ubuntu-22.04","cibw_version": $ver}
          ]
        ')
        echo "include=$FIXED_CI_MATRIX" >> "$GITHUB_OUTPUT"
	echo "platform:" "${FIXED_CI_MATRIX}"
    else
        echo "include=[]" >> "$GITHUB_OUTPUT"
    fi
    cat "$GITHUB_OUTPUT"
    exit 0
fi

generate_matrix_entries() {
    {
        cibuildwheel --print-build-identifiers --platform linux --archs x86_64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" \
            | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "ubuntu-22.04", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform linux --archs aarch64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" \
            | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "ubuntu-22.04-arm", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform macos --archs x86_64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" \
            | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "macos-13", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform macos --archs arm64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" \
            | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "macos-14", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform windows \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" \
            | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "windows-2022", "cibw_version": $ver}'
    }
}

MATRIX=$(generate_matrix_entries | jq -sc)
echo "include=$MATRIX" >> "$GITHUB_OUTPUT"
echo "platform:" "${MATRIX}"
