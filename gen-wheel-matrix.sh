#!/usr/bin/env bash
#set -euo pipefail

CIBW_VERSION="$1"

# Fixed matrix for quick CI smoke tests
FIXED_CI_MATRIX='[{"only":"cp313-manylinux_x86_64","os":"ubuntu-22.04","cibw_version": "3.0.0"},{"only":"cp313-manylinux_aarch64","os":"ubuntu-22.04-arm","cibw_version": "3.0.0"},{"only":"cp313-musllinux_x86_64","os":"ubuntu-22.04","cibw_version": "3.0.0"},{"only":"cp313-musllinux_aarch64","os":"ubuntu-22.04-arm","cibw_version": "3.0.0"},{"only":"cp313-win_amd64","os":"windows-2022","cibw_version": "3.0.0"},{"only":"cp313-win_arm64","os":"windows-2022","cibw_version": "3.0.0"},{"only":"cp313-macosx_x86_64","os":"macos-13","cibw_version": "3.0.0"},{"only":"cp313-macosx_arm64","os":"macos-14","cibw_version": "3.0.0"}]'

# Handle fast CI case
if [[ "${CI_ONLY:-false}" == "true" ]]; then
    if [[ "$CIBW_VERSION" == "3.0.0" ]]; then
	echo "include=$FIXED_CI_MATRIX" >> "$GITHUB_OUTPUT"
    else
	# For 2.23.3 + CI_ONLY, output empty list
	echo "include=[]" >> $GITHUB_OUTPUT
    fi
    cat $GITHUB_OUTPUT
    exit 0
fi

# Decide grep mode based on cibuildwheel version
if [[ "$CIBW_VERSION" == "2.23.3" ]]; then
    GREP_FLAGS=""
    GREP_PATTERN="cp36|cp37"
elif [[ "$CIBW_VERSION" == "3.0.0" ]]; then
    GREP_FLAGS="-v"
    GREP_PATTERN="cp36|cp37"
    CIBW_ENABLE="pypy-eol"  # add `pypy-eol` for newer cibuildwheel
else
    echo "Unsupported cibuildwheel version: $CIBW_VERSION"
    exit 2
fi

generate_matrix_entries() {
    {
        cibuildwheel --print-build-identifiers --platform linux --archs x86_64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "ubuntu-22.04", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform linux --archs aarch64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "ubuntu-22.04-arm", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform macos --archs x86_64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "macos-13", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform macos --archs arm64 \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "macos-14", "cibw_version": $ver}' \
        && cibuildwheel --print-build-identifiers --platform windows \
            | grep $GREP_FLAGS -E "$GREP_PATTERN" | jq -nRc --arg ver "$CIBW_VERSION" '{"only": inputs, "os": "windows-2022", "cibw_version": $ver}'
    }
}

MATRIX=$(generate_matrix_entries | jq -sc)

# Output as GitHub Actions matrix JSON
echo "include=$MATRIX" >> $GITHUB_OUTPUT
echo "platform:" "${MATRIX}"
